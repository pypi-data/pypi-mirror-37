# distutils: language = c++
from random import shuffle

cdef extern from "Fortuna.hpp":
    int _random_range "random_range"(int, int)
    int _random_below "random_below"(int)
    int _d "d"(int)
    int _dice "dice"(int, int)
    int _min_max "min_max"(int, int, int)
    int _percent_true "percent_true"(int)
    int _plus_or_minus "plus_or_minus"(int)
    int _plus_or_minus_linear "plus_or_minus_linear"(int)
    int _plus_or_minus_curve "plus_or_minus_curve"(int)
    int _zero_flat "zero_flat"(int)
    int _zero_cool "zero_cool"(int)
    int _zero_extreme "zero_extreme"(int)
    int _max_cool "max_cool"(int)
    int _max_extreme "max_extreme"(int)
    int _mostly_middle "mostly_middle"(int)
    int _mostly_center "mostly_center"(int)

def random_range(int lo, int hi):
    return _random_range(lo, hi)

def random_below(int num):
    return _random_below(num)

def d(int sides):
    return _d(sides)

def dice(int rolls, int sides):
    assert rolls * sides <= 2147483647, "Value Error, rolls * sides must be <= INT_MAX (2147483647)"
    return _dice(rolls, sides)

def min_max(int n, int lo, int hi):
    return _min_max(n, lo, hi)

def percent_true(int num):
    return _percent_true(num) == 1

def plus_or_minus(int num):
    return _plus_or_minus(num)

def plus_or_minus_linear(int num):
    return _plus_or_minus_linear(num)

def plus_or_minus_curve(int num):
    return _plus_or_minus_curve(num)

def zero_flat(int num):
    return _zero_flat(num)

def zero_cool(int num):
    return _zero_cool(num)

def zero_extreme(int num):
    return _zero_extreme(num)

def max_cool(int num):
    return _max_cool(num)

def max_extreme(int num):
    return _max_extreme(num)

def mostly_middle(int num):
    return _mostly_middle(num)

def mostly_center(int num):
    return _mostly_center(num)

def random_value(arr):
    return arr[random_below(len(arr))]

def pop_random_value(arr):
    return arr.pop(random_below(len(arr)))

def weighted_choice(table):
    max_weight = table[-1][0]
    rand = _random_below(max_weight)
    for weight, value in table:
        if weight > rand:
            return value


class Mostly:
    """ The Quantum Monty """

    def __init__(self, arr):
        size = len(arr)
        assert size > 2, "Size Error: sequence must contain 3 or more items"
        self.__qualname__ = "Mostly"
        self.data = tuple(arr)
        self.max_id = size - 1
        self.methods = (
            self.mostly_first,
            self.mostly_front,
            self.mostly_middle,
            self.mostly_center,
            self.mostly_middle,
            self.mostly_back,
            self.mostly_last
        )

    def mostly_flat(self):
        """ Flat Uniform Distribution """
        return self.data[zero_flat(self.max_id)]

    def mostly_front(self):
        """ Descending Linear Distribution """
        return self.data[zero_cool(self.max_id)]

    def mostly_back(self):
        """ Ascending Linear Distribution """
        return self.data[max_cool(self.max_id)]

    def mostly_middle(self):
        """ Geometric Linear Distribution """
        return self.data[mostly_middle(self.max_id)]

    def mostly_first(self):
        """ Descending Gaussian Distribution """
        return self.data[zero_extreme(self.max_id)]

    def mostly_last(self):
        """ Ascending Gaussian Distribution """
        return self.data[max_extreme(self.max_id)]

    def mostly_center(self):
        """ Geometric Gaussian Distribution """
        return self.data[mostly_center(self.max_id)]

    def __call__(self):
        """ Quantum Monty Algorithm"""
        return random_value(self.methods)()


class RandomCycle:
    """ The Truffle Shuffle """

    def __init__(self, arr):
        assert len(arr) > 2, "Size Error, sequence must contain 3 or more items"
        self.__qualname__ = "RandomCycle"
        self.data = list(arr)
        shuffle(self.data)
        self.next = self.data.pop()
        self.size = len(self.data)

    def __call__(self):
        result = self.next
        self.next = self.data.pop(_max_extreme(self.size - 1))
        self.data.insert(_zero_extreme(self.size - 2), result)
        return result


class WeightedChoice:
    data = ()

    def __call__(self):
        max_weight = self.data[-1][0]
        rand = _random_below(max_weight)
        for weight, value in self.data:
            if weight > rand:
                return value

    @staticmethod
    def _setup(weights, non_unique=False):
        size = len(weights)
        assert size > 0, "Sequence Error, Empty Table"
        if non_unique:
            pass
        else:
            warn_non_unique = (
                "Sanity Check!",
                "  Weighted Values should be unique, pass non_unique=True during instantiation to bypass this check.",
                "  As a result: non-unique values will have their probabilities logically accumulated.",
                "  Relative Weights are summed, Cumulative Weights are over-lapped, but the effect is the same."
            )
            assert size == len(set(v for _, v in weights)), "\n".join(warn_non_unique)

    @staticmethod
    def _optimize(data):
        prev_weight = 0
        for w_pair in data:
            w_pair[0], prev_weight = w_pair[0] - prev_weight, w_pair[0]
        return sorted(data, key=lambda x: x[0], reverse=True)

    @staticmethod
    def _package(data):
        cum_weight = 0
        for w_pair in data:
            cum_weight += w_pair[0]
            w_pair[0] = cum_weight
        return tuple(tuple(itm) for itm in data)


class RelativeWeightedChoice(WeightedChoice):

    def __init__(self, weights, non_unique=False):
        self._setup(weights, non_unique)
        self.__qualname__ = "RelativeWeightedChoice"
        optimized_data = sorted([list(itm) for itm in weights], key=lambda x: x[0], reverse=True)
        self.data = self._package(optimized_data)


class CumulativeWeightedChoice(WeightedChoice):

    def __init__(self, weights, non_unique=False):
        self._setup(weights, non_unique)
        self.__qualname__ = "CumulativeWeightedChoice"
        size = len(weights)
        assert size == len(set(w for w, _ in weights)), "Cumulative Weights must be unique, this is non-negotiable."
        optimized_data = self._optimize(sorted([list(itm) for itm in weights], key=lambda x: x[0]))
        self.data = self._package(optimized_data)
