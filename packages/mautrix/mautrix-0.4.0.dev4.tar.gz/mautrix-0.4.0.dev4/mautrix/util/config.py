from typing import Any, Optional, Tuple, NamedTuple, Callable, Generic, TypeVar, Type
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap
from abc import ABC, abstractmethod

yaml = YAML()
yaml.indent(4)

T = TypeVar('T')


class RecursiveDict(Generic[T]):
    def __init__(self, data: Optional[T] = None, dict_factory: Optional[Type[T]] = None) -> None:
        self._dict_factory = dict_factory or dict
        self._data: CommentedMap = data or self._dict_factory()

    @staticmethod
    def _parse_key(key: str) -> Tuple[str, Optional[str]]:
        if '.' not in key:
            return key, None
        key, next_key = key.split('.', 1)
        if len(key) > 0 and key[0] == "[":
            end_index = next_key.index("]")
            key = key[1:] + "." + next_key[:end_index]
            next_key = next_key[end_index + 2:] if len(next_key) > end_index + 1 else None
        return key, next_key

    def _recursive_get(self, data: T, key: str, default_value: Any) -> Any:
        key, next_key = self._parse_key(key)
        if next_key is not None:
            next_data = data.get(key, self._dict_factory())
            return self._recursive_get(next_data, next_key, default_value)
        return data.get(key, default_value)

    def get(self, key: str, default_value: Any, allow_recursion: bool = True) -> Any:
        if allow_recursion and '.' in key:
            return self._recursive_get(self._data, key, default_value)
        return self._data.get(key, default_value)

    def __getitem__(self, key: str) -> Any:
        return self.get(key, None)

    def __contains__(self, key: str) -> bool:
        return self[key] is not None

    def _recursive_set(self, data: T, key: str, value: Any) -> None:
        key, next_key = self._parse_key(key)
        if next_key is not None:
            if key not in data:
                data[key] = self._dict_factory()
            next_data = data.get(key, self._dict_factory())
            return self._recursive_set(next_data, next_key, value)
        data[key] = value

    def set(self, key: str, value: Any, allow_recursion: bool = True) -> None:
        if allow_recursion and '.' in key:
            self._recursive_set(self._data, key, value)
            return
        self._data[key] = value

    def __setitem__(self, key: str, value: Any) -> None:
        self.set(key, value)

    def _recursive_del(self, data: T, key: str) -> None:
        key, next_key = self._parse_key(key)
        if next_key is not None:
            if key not in data:
                return
            next_data = data[key]
            return self._recursive_del(next_data, next_key)
        try:
            del data[key]
            del data.ca.items[key]
        except KeyError:
            pass

    def delete(self, key: str, allow_recursion: bool = True) -> None:
        if allow_recursion and '.' in key:
            self._recursive_del(self._data, key)
            return
        try:
            del self._data[key]
            del self._data.ca.items[key]
        except KeyError:
            pass

    def __delitem__(self, key: str) -> None:
        self.delete(key)


ConfigUpdateHelper = NamedTuple("ConfigUpdateHelper",
                                base=RecursiveDict[CommentedMap],
                                copy=Callable[[str, str], None],
                                copy_dict=Callable[[str, str, bool], None])


class BaseConfig(ABC, RecursiveDict[CommentedMap]):
    def __init__(self, path: str, base_path: str) -> None:
        super().__init__()
        self.path: str = path
        self.base_path: str = base_path

    def load(self) -> None:
        with open(self.path, 'r') as stream:
            self._data = yaml.load(stream)

    def load_base(self) -> Optional[RecursiveDict[CommentedMap]]:
        try:
            with open(self.base_path, 'r') as stream:
                return RecursiveDict(yaml.load(stream))
        except OSError:
            pass
        return None

    def save(self) -> None:
        with open(self.path, 'w') as stream:
            yaml.dump(self._data, stream)

    def _pre_update(self) -> Optional[ConfigUpdateHelper]:
        base = self.load_base()
        if not base:
            return None

        def copy(from_path: str, to_path: str = None) -> None:
            if from_path in self:
                base[to_path or from_path] = self[from_path]

        def copy_dict(from_path: str, to_path: str = None,
                      override_existing_map: bool = True) -> None:
            if from_path in self:
                to_path = to_path or from_path
                if override_existing_map or to_path not in base:
                    base[to_path] = CommentedMap()
                for key, value in self[from_path].items():
                    base[to_path][key] = value

        return ConfigUpdateHelper(base, copy, copy_dict)

    @abstractmethod
    def update(self) -> None:
        pass
