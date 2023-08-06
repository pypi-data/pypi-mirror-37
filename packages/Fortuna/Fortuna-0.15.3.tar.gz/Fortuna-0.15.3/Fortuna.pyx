# distutils: language = c++

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

cdef int INT_MAX = 1000000000
cdef int INT_MIN = -1000000000

def random_range(int lo, int hi):
    assert INT_MIN <= lo <= INT_MAX, f"Input Error, out of range ({INT_MIN}..{INT_MAX})."
    assert INT_MIN <= hi <= INT_MAX, f"Input Error, out of range ({INT_MIN}..{INT_MAX})."
    return _random_range(lo, hi)

def random_below(int num):
    assert INT_MIN <= num <= INT_MAX, f"Input Error, out of range ({INT_MIN}..{INT_MAX})."
    return _random_below(num)

def d(int sides):
    assert 1 <= sides <= INT_MAX, f"Input Error, out of range (1..{INT_MAX})."
    return _d(sides)

def dice(int rolls, int sides):
    max_rolls = 10000000
    assert rolls <= max_rolls, f"Input Error, out of range (1..{max_rolls})."
    assert 1 <= rolls * sides <= INT_MAX * 2, f"Input Error, product of input args (rolls * sides) out of range (1..{INT_MAX * 2})."
    return _dice(rolls, sides)

def min_max(int n, int lo, int hi):
    input_data = (n, lo, hi)
    for itm in input_data:
        assert INT_MIN <= itm <= INT_MAX, f"Input Error, out of range ({INT_MIN}..{INT_MAX})."
    return _min_max(n, lo, hi)

def percent_true(int num):
    assert 0 <= num <= 100, f"Input Error, out of range (0..100)."
    return _percent_true(num) == 1

def plus_or_minus(int num):
    assert INT_MIN <= num <= INT_MAX, f"Input Error, out of range ({INT_MIN}..{INT_MAX})."
    return _plus_or_minus(num)

def plus_or_minus_linear(int num):
    assert INT_MIN <= num <= INT_MAX, f"Input Error, out of range ({INT_MIN}..{INT_MAX})."
    return _plus_or_minus_linear(num)

def plus_or_minus_curve(int num):
    assert INT_MIN <= num <= INT_MAX, f"Input Error, out of range ({INT_MIN}..{INT_MAX})."
    return _plus_or_minus_curve(num)

def zero_flat(int num):
    assert INT_MIN <= num <= INT_MAX, f"Input Error, out of range ({INT_MIN}..{INT_MAX})."
    return _zero_flat(num)

def zero_cool(int num):
    assert INT_MIN <= num <= INT_MAX, f"Input Error, out of range ({INT_MIN}..{INT_MAX})."
    return _zero_cool(num)

def zero_extreme(int num):
    assert INT_MIN <= num <= INT_MAX, f"Input Error, out of range ({INT_MIN}..{INT_MAX})."
    return _zero_extreme(num)

def max_cool(int num):
    assert INT_MIN <= num <= INT_MAX, f"Input Error, out of range ({INT_MIN}..{INT_MAX})."
    return _max_cool(num)

def max_extreme(int num):
    assert INT_MIN <= num <= INT_MAX, f"Input Error, out of range ({INT_MIN}..{INT_MAX})."
    return _max_extreme(num)

def mostly_middle(int num):
    assert INT_MIN <= num <= INT_MAX, f"Input Error, out of range ({INT_MIN}..{INT_MAX})."
    return _mostly_middle(num)

def mostly_center(int num):
    assert INT_MIN <= num <= INT_MAX, f"Input Error, out of range ({INT_MIN}..{INT_MAX})."
    return _mostly_center(num)

def random_value(arr):
    assert 1 <= len(arr) <= INT_MAX, f"Input Error, sequence length out of range (1..{INT_MAX})."
    return arr[random_below(len(arr))]

def pop_random_value(arr):
    assert 1 <= len(arr) <= INT_MAX, f"Input Error, sequence length out of range (1..{INT_MAX})."
    return arr.pop(random_below(len(arr)))

def weighted_choice(table):
    assert 1 <= len(table) <= INT_MAX, f"Input Error, sequence length out of range (1..{INT_MAX})."
    max_weight = table[-1][0]
    rand = _random_below(max_weight)
    for weight, value in table:
        if weight > rand:
            return value


class Mostly:
    """ The Quantum Monty """

    def __init__(self, arr):
        size = len(arr)
        assert 3 <= size <= INT_MAX, f"Input Error, sequence length out of range (3..{INT_MAX})."
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
        return self.data[zero_flat(self.max_id)]

    def mostly_front(self):
        return self.data[zero_cool(self.max_id)]

    def mostly_back(self):
        return self.data[max_cool(self.max_id)]

    def mostly_middle(self):
        return self.data[mostly_middle(self.max_id)]

    def mostly_first(self):
        return self.data[zero_extreme(self.max_id)]

    def mostly_last(self):
        return self.data[max_extreme(self.max_id)]

    def mostly_center(self):
        return self.data[mostly_center(self.max_id)]

    def __call__(self):
        return random_value(self.methods)()


class RandomCycle:

    def __init__(self, arr):
        from random import shuffle
        assert 3 <= len(arr) <= INT_MAX, f"Input Error, sequence length out of range (3..{INT_MAX})."
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
        if non_unique:
            pass
        else:
            size = len(weights)
            warn_non_unique = (
                "Sanity Check!",
                "  Weighted Values should be unique, pass non_unique=True during instantiation to bypass this check.",
                "  As a result: non-unique values will have their probabilities logically accumulated.",
                "  Relative Weights are summed, Cumulative Weights are over-lapped, but the effect is the same.",
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
        size = len(weights)
        assert 1 <= size <= INT_MAX, f"Input Error, sequence length out of range (1..{INT_MAX})."
        self._setup(weights, non_unique)
        optimized_data = sorted([list(itm) for itm in weights], key=lambda x: x[0], reverse=True)
        self.data = self._package(optimized_data)


class CumulativeWeightedChoice(WeightedChoice):

    def __init__(self, weights, non_unique=False):
        size = len(weights)
        assert 1 <= size <= INT_MAX, f"Input Error, sequence length out of range (1..{INT_MAX})."
        assert size == len(set(w for w, _ in weights)), "Cumulative Weights must be unique, because math."
        self._setup(weights, non_unique)
        optimized_data = self._optimize(sorted([list(itm) for itm in weights], key=lambda x: x[0]))
        self.data = self._package(optimized_data)
