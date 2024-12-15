import pytest

from src.planetae_orm.models import meta


@pytest.fixture
def Test1():
    class Test1(metaclass=meta.MetaSingleton):
        def __init__(self) -> None:
            pass

    return Test1


@pytest.fixture
def t1(Test1):
    return Test1()


@pytest.fixture
def Test3():
    class Test3(metaclass=meta.AbstractMetaSingleton):
        def __init__(self):
            super().__init__()

    return Test3


@pytest.fixture
def t5(Test3):
    return Test3()
