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

    class Test1(metaclass=MetaSingleton):
        def __init__(self) -> None:
            pass

    t1 = Test1()
    t2 = Test1()
    print(t1)
    print(t2)
    print(t1 is t2)

    class Test2(Test1):
        def __init__(self) -> None:
            super().__init__()

    t3 = Test2()
    t4 = Test2()
    print(t3)
    print(t4)
    print(t3 is t4)
    print(t3 is t1)

    class Test3(metaclass=AbstractMetaSingleton):
        def __init__(self):
            super().__init__()

    class Test4(Test3):
        def __init__(self):
            super().__init__()

    t5 = Test3()
    t6 = Test3()
    print(t5)
    print(t6)
    print(t5 is t6)

    t7 = Test4()
    t8 = Test4()
    print(t7)
    print(t8)
    print(t7 is t8)
    print(t6 is t7)
