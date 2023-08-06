from Fortuna import *
import random  # Base Cases (randrange, randint and choice) for comparison only
from datetime import datetime


def distribution_timer(func: staticmethod, *args, call_sig):
    num_cycles = 100000
    start_time = datetime.now()
    results = [func(*args) for _ in range(num_cycles)]
    end_time = datetime.now()
    total_time = (end_time - start_time).total_seconds()
    print(f"{call_sig} x {num_cycles}: {round(total_time * 1000.0, 2)} ms")
    result_obj = {key: f"{round(results.count(key) / (num_cycles / 100), 2)}%" for key in sorted(list(set(results)))}
    for key, val in result_obj.items():
        print(f" {key}: {val}")
    print("")


if __name__ == "__main__":

    t0 = datetime.now()
    print("Fortuna 0.15 Sample Distribution and Performance Test Suite")
    print("\nRandom Numbers")
    print(f"{'-' * 73}\n")
    distribution_timer(random.randrange, 10, call_sig="Base Case:\nrandom.randrange(10)")
    distribution_timer(random.randint, 1, 10, call_sig="Base Case:\nrandom.randint(1, 10)")
    distribution_timer(random_range, 1, 10, call_sig="random_range(1, 10)"),
    distribution_timer(d, 6, call_sig="d(6)"),
    distribution_timer(dice, 2, 6, call_sig="dice(2, 6)"),
    distribution_timer(plus_or_minus, 5, call_sig="plus_or_minus(5)"),
    distribution_timer(plus_or_minus_linear, 5, call_sig="plus_or_minus_linear(5)"),
    distribution_timer(plus_or_minus_curve, 5, call_sig="plus_or_minus_curve(5)"),
    print("\nRandom Truthy")
    print(f"{'-' * 73}\n")
    distribution_timer(percent_true, 25, call_sig="percent_true(25)")
    print("\nRandom List Values")
    print(f"{'-' * 73}\n")
    some_list = ["Alpha", "Beta", "Delta", "Eta", "Gamma", "Kappa", "Zeta"]
    distribution_timer(random.choice, some_list, call_sig="Base Case:\nrandom.choice(some_list)")
    distribution_timer(random_value, some_list, call_sig="random_value(some_list)")
    M = Mostly(some_list)
    distribution_timer(M.mostly_front, call_sig="M.mostly_front()")
    distribution_timer(M.mostly_middle, call_sig="M.mostly_middle()")
    distribution_timer(M.mostly_back, call_sig="M.mostly_back()")
    distribution_timer(M.mostly_first, call_sig="M.mostly_first()")
    distribution_timer(M.mostly_center, call_sig="M.mostly_center()")
    distribution_timer(M.mostly_last, call_sig="M.mostly_last")
    distribution_timer(M, call_sig="M()")
    RC = RandomCycle(some_list)
    distribution_timer(RC, call_sig="RC()")
    print("\nRandom Values by Weighted Table")
    print(f"{'-' * 73}\n")
    cumulative_weighted_table = (
        (7, "Apple"),
        (11, "Banana"),
        (13, "Cherry"),
        (23, "Grape"),
        (26, "Lime"),
        (30, "Orange"),
    )
    cumulative_weighted_choice = CumulativeWeightedChoice(cumulative_weighted_table)
    distribution_timer(cumulative_weighted_choice, call_sig="cumulative_weighted_choice()")
    relative_weighted_table = (
        (7, "Apple"),
        (4, "Banana"),
        (2, "Cherry"),
        (10, "Grape"),
        (3, "Lime"),
        (4, "Orange"),
    )
    relative_weighted_choice = RelativeWeightedChoice(relative_weighted_table)
    distribution_timer(relative_weighted_choice, call_sig="relative_weighted_choice()")
    print(f"\n{'-' * 73}")
    total_test_time = round((datetime.now() - t0).total_seconds(), 2)
    print(f"Total Test Time: {total_test_time} sec")
