from Fortuna import *
import random  # Base Cases (randrange, randint and choice) for comparison only
from datetime import datetime


def distribution_timer(func: staticmethod, *args, call_sig=None):
    num_cycles = 100000
    start_time = datetime.now()
    results = [func(*args) for _ in range(num_cycles)]
    end_time = datetime.now()
    if not call_sig:
        func_name = f"{func.__qualname__}"
        arg = f"({args[0]})" if len(args) == 1 else args
        func_call_str = f"{func_name}{arg}"
    else:
        func_call_str = call_sig
    total_time = (end_time - start_time).total_seconds()
    print(f"{func_call_str} x {num_cycles}: {round(total_time * 1000.0, 2)} ms")
    result_obj = {key: f"{round(results.count(key) / (num_cycles / 100), 2)}%" for key in sorted(list(set(results)))}
    for key, val in result_obj.items():
        print(f" {key}: {val}")
    print("")


if __name__ == "__main__":
    t0 = datetime.now()
    print("Fortuna 0.14 Sample Distribution and Performance Test Suite")
    print("\nRandom Numbers")
    print(f"{'-' * 73}\n")
    distribution_timer(random.randrange, 10, call_sig="Base Case:\nrandom.randrange(10)")
    distribution_timer(random.randint, 1, 10, call_sig="Base Case:\nrandom.randint(1, 10)")
    numeric_func_calls = (
        (random_range, 1, 10),
        (d, 6),
        (dice, 2, 6),
        (plus_or_minus, 5),
        (plus_or_minus_linear, 5),
        (plus_or_minus_curve, 5),
    )
    for func_call in numeric_func_calls:
        distribution_timer(*func_call)
    print("\nRandom Truth")
    print(f"{'-' * 73}\n")
    distribution_timer(percent_true, 25)
    print("\nRandom List Values")
    print(f"{'-' * 73}\n")
    some_list = ["Alpha", "Beta", "Delta", "Eta", "Gamma", "Kappa", "Zeta"]
    distribution_timer(random.choice, some_list, call_sig="Base Case:\nrandom.choice(some_list)")
    distribution_timer(random_value, some_list, call_sig="random_value(some_list)")
    M = Mostly(some_list)
    distribution_timer(M.mostly_front)
    distribution_timer(M.mostly_middle)
    distribution_timer(M.mostly_back)
    distribution_timer(M.mostly_first)
    distribution_timer(M.mostly_center)
    distribution_timer(M.mostly_last)
    distribution_timer(M)
    RC = RandomCycle(some_list)
    distribution_timer(RC)
    print("\nRandom Values by Weighted Table")
    print(f"{'-' * 73}\n")
    relative_weighted_table = (
        (7, "Apple"),
        (4, "Banana"),
        (2, "Cherry"),
        (10, "Grape"),
        (3, "Lime"),
        (4, "Orange"),
    )
    relative_weighted_choice = RelativeWeightedChoice(relative_weighted_table)
    distribution_timer(relative_weighted_choice)
    cumulative_weighted_table = (
        (7, "Apple"),
        (11, "Banana"),
        (13, "Cherry"),
        (23, "Grape"),
        (26, "Lime"),
        (30, "Orange"),
    )
    cumulative_weighted_choice = CumulativeWeightedChoice(cumulative_weighted_table)
    distribution_timer(cumulative_weighted_choice)
    print(f"\n{'-' * 73}")
    total_test_time = round((datetime.now() - t0).total_seconds(), 2)
    print(f"Total Test Time: {total_test_time} sec")
