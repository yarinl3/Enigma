from sort_algos import Sorts
import enigma


def integer_sort_test():
    myobject1 = Sorts([-100, 10, -10])
    assert myobject1.merge_sort() == [-101, -100, 10]
