from Fortuna import *
import random  # Base Cases (randrange, randint and choice) for comparison only
from datetime import datetime
from math import floor


def distribution_timer(func: staticmethod, *args, call_sig="f(x)", max_distribution=20):
    num_cycles = 100000
    start_time = datetime.now()
    results = [func(*args) for _ in range(num_cycles)]
    end_time = datetime.now()
    total_time = (end_time - start_time).total_seconds()
    print(f"{call_sig} x {num_cycles}: {round(total_time * 1000.0, 2)} ms")
    unique_results = set(results)
    if len(unique_results) <= max_distribution:
        result_obj = {
            key: f"{round(results.count(key) / (num_cycles / 100), 2)}%" for key in sorted(list(unique_results))
        }
        for key, val in result_obj.items():
            print(f" {key}: {val}")
    print("")


def floor_dice(rolls, sides):
    """ Fast but poor distribution properties, can cause platform dependant bias. """
    total = rolls
    for _ in range(rolls):
        total += floor(random.random() * sides)
    return total


def randrange_dice(rolls, sides):
    """ Slow but good distribution properties. """
    total = rolls
    for _ in range(rolls):
        total += random.randrange(sides)
    return total


if __name__ == "__main__":

    t0 = datetime.now()
    print("Fortuna 0.15.2 Sample Distribution and Performance Test Suite\n")

    print("Random Numbers")
    print(f"{'-' * 73}\n")
    distribution_timer(random.randrange, 10, call_sig="Base Case:\nrandom.randrange(10)")
    distribution_timer(random_below, 10, call_sig="Fortuna.random_below(10)")
    distribution_timer(random.randint, 1, 10, call_sig="Base Case:\nrandom.randint(1, 10)")
    distribution_timer(random_range, 1, 10, call_sig="Fortuna.random_range(1, 10)")
    distribution_timer(d, 10, call_sig="Fortuna.d(10)")
    distribution_timer(dice, 1, 10, call_sig="Fortuna.dice(1, 10)")
    distribution_timer(plus_or_minus, 5, call_sig="Fortuna.plus_or_minus(5)")
    distribution_timer(plus_or_minus_linear, 5, call_sig="Fortuna.plus_or_minus_linear(5)")
    distribution_timer(plus_or_minus_curve, 5, call_sig="Fortuna.plus_or_minus_curve(5)")
    print("")

    print("Random Truth")
    print(f"{'-' * 73}\n")
    distribution_timer(percent_true, 25, call_sig="Fortuna.percent_true(25)")
    print("")

    print("Random Values from a Sequence")
    print(f"{'-' * 73}\n")
    some_list = ["Alpha", "Beta", "Delta", "Eta", "Gamma", "Kappa", "Zeta"]
    print(f"some_list = {some_list}\n")
    distribution_timer(random.choice, some_list, call_sig="Base Case:\nrandom.choice(some_list)")
    distribution_timer(random_value, some_list, call_sig="Fortuna.random_value(some_list)")
    monty = Mostly(some_list)
    print(f"monty = Mostly(some_list)\n")
    distribution_timer(monty.mostly_front, call_sig="monty.mostly_front()")
    distribution_timer(monty.mostly_middle, call_sig="monty.mostly_middle()")
    distribution_timer(monty.mostly_back, call_sig="monty.mostly_back()")
    distribution_timer(monty.mostly_first, call_sig="monty.mostly_first()")
    distribution_timer(monty.mostly_center, call_sig="monty.mostly_center()")
    distribution_timer(monty.mostly_last, call_sig="monty.mostly_last()")
    distribution_timer(monty, call_sig="monty()")
    truffle_shuffle = RandomCycle(some_list)
    print(f"truffle_shuffle = RandomCycle(some_list)\n")
    distribution_timer(truffle_shuffle, call_sig="truffle_shuffle()")
    print("")

    print("Random Values by Weighted Table")
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
    print("")

    r, s = 10, 10
    print(f"Multi Dice: {r}d{s}")
    print(f"{'-' * 73}\n")
    distribution_timer(randrange_dice, r, s, call_sig=f"Base Case:\nrandrange_dice({r}, {s})"),
    distribution_timer(floor_dice, r, s, call_sig=f"Base Case:\nfloor_dice({r}, {s})"),
    distribution_timer(dice, r, s, call_sig=f"Fortuna.dice({r}, {s})"),
    print("")

    print(f"{'-' * 73}")
    total_test_time = round((datetime.now() - t0).total_seconds(), 2)
    print(f"Total Test Time: {total_test_time} sec\n")
