from typing import Dict, List, Callable, Union, Optional, Awaitable
import asyncio

from ..errors import MatrixRequestError
from ..api import JSON
from .api.types import EventType, StateEvent, Event, FilterID, Filter
from .api import ClientAPI
from .store import ClientStore, MemoryClientStore

EventHandler = Callable[[Event], Awaitable[None]]


class Client(ClientAPI):
    def __init__(self, *args, store: ClientStore = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.log = self.api.log
        self.store = store or MemoryClientStore()
        self.global_event_handlers: List[EventHandler] = []
        self.event_handlers: Dict[EventType, List[EventHandler]] = {}
        self.syncing_id: int = 0

    def on(self, var: Union[EventHandler, EventType]
           ) -> Union[EventHandler, Callable[[EventHandler], EventHandler]]:
        if isinstance(var, EventType):
            def decorator(func: EventHandler) -> EventHandler:
                self.add_event_handler(func, var)
                return func

            return decorator
        else:
            self.add_event_handler(var)
            return var

    def add_event_handler(self, handler: EventHandler, event_type: Optional[EventType] = None
                          ) -> None:
        if not isinstance(event_type, EventType):
            self.global_event_handlers.append(handler)
        else:
            self.event_handlers.setdefault(event_type, []).append(handler)

    def remove_event_handler(self, handler: EventHandler, event_type: Optional[EventType] = None
                             ) -> None:
        try:
            if not isinstance(event_type, EventType):
                self.global_event_handlers.remove(handler)
            else:
                handlers = self.event_handlers[event_type]
                handlers.remove(handler)
                if len(handlers) == 0:
                    del self.event_handlers[event_type]
        except (KeyError, ValueError):
            pass

    async def call_handlers(self, event: Event) -> None:
        event._client = self
        for handler in self.global_event_handlers + self.event_handlers.get(event.type, []):
            try:
                await handler(event)
            except Exception:
                self.log.exception("Failed to run handler")

    def handle_sync(self, data: JSON) -> None:
        rooms = data.get("rooms", {})
        for room_id, room_data in rooms.get("join", {}).items():
            for raw_event in room_data.get("state", {}).get("events", []):
                raw_event["room_id"] = room_id
                asyncio.ensure_future(self.call_handlers(StateEvent.deserialize(raw_event)),
                                      loop=self.loop)

            for raw_event in room_data.get("timeline", {}).get("events", []):
                raw_event["room_id"] = room_id
                asyncio.ensure_future(self.call_handlers(Event.deserialize(raw_event)),
                                      loop=self.loop)
        for room_id, room_data in rooms.get("invite", {}).items():
            for raw_event in room_data.get("state", {}).get("events", []):
                raw_event["room_id"] = room_id
                asyncio.ensure_future(self.call_handlers(StateEvent.deserialize(raw_event)),
                                      loop=self.loop)
        for room_id, room_data in rooms.get("leave", {}).items():
            for raw_event in room_data.get("timeline", {}).get("events", []):
                if "state_key" in raw_event:
                    raw_event["room_id"] = room_id
                    asyncio.ensure_future(self.call_handlers(StateEvent.deserialize(raw_event)),
                                          loop=self.loop)

    async def start(self, filter_data: Optional[Union[FilterID, Filter]] = None) -> None:
        if isinstance(filter_data, Filter):
            filter_data = await self.create_filter(filter_data)

        self.syncing_id += 1
        this_sync_id = self.syncing_id
        fail_sleep = 5

        while this_sync_id == self.syncing_id:
            try:
                data = await self.sync(since=self.store.next_batch, filter_id=filter_data)
                fail_sleep = 5
            except MatrixRequestError:
                self.log.exception(f"Sync request errored, waiting {fail_sleep}"
                                       " seconds before continuing")
                await asyncio.sleep(fail_sleep, loop=self.loop)
                if fail_sleep < 80:
                    fail_sleep *= 2
                continue

            if this_sync_id != self.syncing_id:
                break
            self.store.next_batch = data.get("next_batch")
            try:
                self.handle_sync(data)
            except Exception:
                self.log.exception("Sync handling errored")

    def stop(self) -> None:
        self.syncing_id += 1
