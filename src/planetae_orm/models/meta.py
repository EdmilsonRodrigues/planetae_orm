from abc import ABCMeta
from typing import Any


class MetaSingleton(type):
    _instances: dict[type, object] = {}

    def __call__(cls, *args, **kwds) -> Any:
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwds)
        return cls._instances[cls]


class AbstractMetaSingleton(MetaSingleton, ABCMeta):
    pass


if __name__ == '__main__':
    pass
