#!python3
#distutils: language = c++
from collections import OrderedDict
from random import shuffle
from datetime import datetime


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
    int _fast_rand_below "fast_rand_below"(int)
    int _fast_d "fast_d"(int)
    int _fast_dice "fast_dice"(int, int)


def random_range(int lo, int hi) -> int:
    return _random_range(lo, hi)

def random_below(int num) -> int:
    return _random_below(num)

def fast_rand_below(int num) -> int:
    return _fast_rand_below(num)

def fast_d(int sides) -> int:
    return _fast_d(sides)

def fast_dice(int rolls, int sides) -> int:
    return _fast_dice(rolls, sides)

def d(int sides) -> int:
    assert sides >= 1, f"Input Error, 'sides' must be >= 1."
    return _d(sides)

def dice(int rolls, int sides) -> int:
    assert rolls >= 1 and sides >= 1, f"Input Error, 'rolls' & 'sides' must be >= 1."
    return _dice(rolls, sides)

def min_max(int n, int lo, int hi) -> int:
    return _min_max(n, lo, hi)

def percent_true(int num) -> bool:
    return _percent_true(_min_max(num, 0, 100)) == 1

def plus_or_minus(int num) -> int:
    return _plus_or_minus(num)

def plus_or_minus_linear(int num) -> int:
    return _plus_or_minus_linear(num)

def plus_or_minus_curve(int num) -> int:
    return _plus_or_minus_curve(num)

def zero_flat(int num) -> int:
    return _zero_flat(num)

def zero_cool(int num) -> int:
    return _zero_cool(num)

def zero_extreme(int num) -> int:
    return _zero_extreme(num)

def max_cool(int num) -> int:
    return _max_cool(num)

def max_extreme(int num) -> int:
    return _max_extreme(num)

def mostly_middle(int num) -> int:
    return _mostly_middle(num)

def mostly_center(int num) -> int:
    return _mostly_center(num)

def random_value(arr) -> object:
    assert len(arr) >= 1, f"Input Error, sequence must not be empty."
    idx = _random_below(len(arr))
    return arr[idx]

def pop_random_value(arr) -> object:
    assert len(arr) >= 1, f"Input Error, sequence must not be empty."
    idx = _random_below(len(arr))
    return arr.pop(idx)

def cumulative_weighted_choice(table) -> object:
    assert len(table) >= 1, f"Input Error, sequence must not be empty."
    max_weight = table[-1][0]
    rand = _random_below(max_weight)
    for weight, value in table:
        if weight > rand:
            return value


class Mostly:
    """ The Quantum Monty """
    __slots__ = ("data", "max_id", "methods")

    def __init__(self, arr):
        size = len(arr)
        assert size >= 3, f"Input Error, sequence length must be >= 3."
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

    def mostly_flat(self) -> object:
        return self.data[_zero_flat(self.max_id)]

    def mostly_front(self) -> object:
        return self.data[_zero_cool(self.max_id)]

    def mostly_back(self) -> object:
        return self.data[_max_cool(self.max_id)]

    def mostly_middle(self) -> object:
        return self.data[_mostly_middle(self.max_id)]

    def mostly_first(self) -> object:
        return self.data[_zero_extreme(self.max_id)]

    def mostly_last(self) -> object:
        return self.data[_max_extreme(self.max_id)]

    def mostly_center(self) -> object:
        return self.data[_mostly_center(self.max_id)]

    def __call__(self) -> object:
        return random_value(self.methods)()


class RandomCycle:
    __slots__ = ("data", "next", "size")

    def __init__(self, arr):
        self.size = len(arr)
        assert self.size >= 3, f"Input Error, sequence length must be >= 3."
        self.data = list(arr)
        shuffle(self.data)
        self.next = self.data.pop()
        self.size -= 1

    def __call__(self) -> object:
        result = self.next
        self.next = self.data.pop(_max_extreme(self.size - 1))
        self.data.insert(_zero_extreme(self.size - 2), result)
        return result


class WeightedChoice:

    def __call__(self) -> object:
        return cumulative_weighted_choice(self.data)

    @staticmethod
    def _setup(weighted_table, is_cumulative, non_unique=False):
        size = len(weighted_table)
        assert size >= 1, f"Input Error, sequence length must be >= 1."
        if is_cumulative:
            assert size == len(set(w for w, _ in weighted_table)), "Cumulative Weights must be unique, because math."
        if non_unique:
            pass
        else:
            warn_non_unique = (
                "Sanity Check!",
                "  Weighted Values should be unique, pass non_unique=True during instantiation to bypass this check.",
                "  As a result: non-unique values will have their probabilities logically accumulated.",
                "  Relative Weights are summed, Cumulative Weights are over-lapped, but the effect is the same.",
            )
            assert size == len(set(v for _, v in weighted_table)), "\n".join(warn_non_unique)

    @staticmethod
    def _optimize(weighted_table, is_cumulative) -> list:
        if not is_cumulative:
            return sorted([list(itm) for itm in weighted_table], key=lambda x: x[0], reverse=True)
        else:
            data = sorted([list(itm) for itm in weighted_table], key=lambda x: x[0])
            prev_weight = 0
            for w_pair in data:
                w_pair[0], prev_weight = w_pair[0] - prev_weight, w_pair[0]
            return sorted(data, key=lambda x: x[0], reverse=True)

    @staticmethod
    def _package(data) -> tuple:
        cum_weight = 0
        for w_pair in data:
            cum_weight += w_pair[0]
            w_pair[0] = cum_weight
        return tuple(tuple(itm) for itm in data)


class RelativeWeightedChoice(WeightedChoice):

    def __init__(self, weighted_table, non_unique=False):
        size = len(weighted_table)
        self._setup(weighted_table, is_cumulative=False, non_unique=non_unique)
        optimized_data = self._optimize(weighted_table, is_cumulative=False)
        self.data = self._package(optimized_data)


class CumulativeWeightedChoice(WeightedChoice):

    def __init__(self, weighted_table, non_unique=False):
        self._setup(weighted_table, is_cumulative=True, non_unique=non_unique)
        optimized_data = self._optimize(weighted_table, is_cumulative=True)
        self.data = self._package(optimized_data)


class MultiCat:
    __slots__ = ("cat_data", "cat_keys", "random_cat")

    def __init__(self, cat_data):
        assert len(cat_data) >= 3, f"Input Error, sequence length must be >= 3."
        self.cat_data = OrderedDict(
            {key: RandomCycle(itm) for key, itm in cat_data.items()}
        )
        self.cat_keys = tuple(self.cat_data.keys())
        self.random_cat = Mostly(self.cat_keys).mostly_front

    def __call__(self, cat_key=None) -> object:
        if not cat_key:
            return self.cat_data[self.random_cat()]()
        assert cat_key in self.cat_keys, f"Key Error, '{cat_key}' not in cat_keys: {self.cat_keys}"
        return self.cat_data[cat_key]()


def distribution_timer(func: staticmethod, *args, call_sig="f(x)", max_distribution=25, **kwargs):
    num_cycles = 1000000
    start_time = datetime.now()
    results = [func(*args, **kwargs) for _ in range(num_cycles)]
    end_time = datetime.now()
    total_time = (end_time - start_time).total_seconds()
    print(f"{call_sig} x {num_cycles}: {round(total_time * 1000.0, 2)} ms")
    if type(results[0]) is list:
        for i, _ in enumerate(results):
            results[i] = results[i][0]
    unique_results = set(results)
    if len(unique_results) <= max_distribution:
        result_obj = {
            key: f"{round(results.count(key) / (num_cycles / 100), 2)}%" for key in sorted(list(unique_results))
        }
        for key, val in result_obj.items():
            print(f" {key}: {val}")
    print("")
