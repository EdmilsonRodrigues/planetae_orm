def test_meta_singleton(Test1, t1):
    t2 = Test1()
    assert t1 is t2
    assert t1 == t2


def test_subclass_meta_singleton(Test1, t1):
    class Test2(Test1):
        def __init__(self) -> None:
            super().__init__()

    t3 = Test2()
    t4 = Test2()
    assert t3 is t4
    assert t3 == t4
    assert t3 is not t1
    assert t3 != t1


def test_abstract_meta_singleton(Test3, t5):
    t6 = Test3()
    assert t5 is t6
    assert t5 == t6


def test_subclass_abstract_meta_singleton(Test3, t5):
    class Test4(Test3):
        def __init__(self):
            super().__init__()

    t7 = Test4()
    t8 = Test4()

    assert t7 == t8
    assert t7 is t8
    assert t7 is not t5
    assert t7 != t5
