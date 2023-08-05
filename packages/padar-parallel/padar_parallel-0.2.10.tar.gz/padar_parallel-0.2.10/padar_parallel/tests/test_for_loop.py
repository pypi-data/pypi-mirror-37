from ..for_loop import ForLoop


def test_forloop():
    def func(data):
        return abs(data)

    def merge_func(data_list):
        return sum(data_list)

    data_list = list(range(-10, 11))

    for_loop = ForLoop(func, merge_func, data_list)

    for_loop.compute()

    assert for_loop.get_result() == 110
