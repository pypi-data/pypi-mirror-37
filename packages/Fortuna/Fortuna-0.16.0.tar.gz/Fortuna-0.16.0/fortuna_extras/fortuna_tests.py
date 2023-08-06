from Fortuna import *
from datetime import datetime
from collections import OrderedDict
import random  # Base Cases (randrange, randint, random, choice and choices) for comparison only
from math import floor  # Base Case floor_dice


def floor_dice(rolls: int, sides: int) -> int:
    """ Base Case """
    total = rolls
    for _ in range(rolls):
        total += floor(random.random() * sides)
    return total


def randrange_dice(rolls: int, sides: int) -> int:
    """ Base Case """
    total = rolls
    for _ in range(rolls):
        total += random.randrange(sides)
    return total


def randint_dice(rolls: int, sides: int) -> int:
    """ Base Case """
    total = 0
    for _ in range(rolls):
        total += random.randint(1, sides)
    return total


if __name__ == "__main__":
    t0 = datetime.now()
    print("Fortuna 0.16.0 Sample Distribution and Performance Test Suite\n")
    print("Random Numbers")
    print(f"{'-' * 73}\n")
    distribution_timer(random.randint, 1, 10, call_sig="Base Case:\nrandom.randint(1, 10)")
    distribution_timer(random_range, 1, 10, call_sig="Fortuna.random_range(1, 10)")
    distribution_timer(random.randrange, 10, call_sig="Base Case:\nrandom.randrange(10)")
    distribution_timer(random_below, 10, call_sig="Fortuna.random_below(10)")
    distribution_timer(fast_rand_below, 10, call_sig="Fast Base Case:\nFortuna.fast_rand_below(10)")
    distribution_timer(d, 10, call_sig="Fortuna.d(10)")
    distribution_timer(fast_d, 10, call_sig="Fast Base Case:\nFortuna.fast_d(10)")
    distribution_timer(dice, 1, 10, call_sig="Fortuna.dice(1, 10)")
    distribution_timer(fast_dice, 1, 10, call_sig="Fast Base Case:\nFortuna.fast_dice(1, 10)")
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
    distribution_timer(random.choice, some_list, call_sig="Base Case:\nrandom.choice(some_list)")
    distribution_timer(random_value, some_list, call_sig="Fortuna.random_value(some_list)")

    mostly = Mostly(some_list)
    distribution_timer(mostly.mostly_front, call_sig="mostly.mostly_front()")
    distribution_timer(mostly.mostly_middle, call_sig="mostly.mostly_middle()")
    distribution_timer(mostly.mostly_back, call_sig="mostly.mostly_back()")
    distribution_timer(mostly.mostly_first, call_sig="mostly.mostly_first()")
    distribution_timer(mostly.mostly_center, call_sig="mostly.mostly_center()")
    distribution_timer(mostly.mostly_last, call_sig="mostly.mostly_last()")
    distribution_timer(mostly, call_sig="mostly()")
    random_cycle = RandomCycle(some_list)
    distribution_timer(random_cycle, call_sig="random_cycle()")
    print("")

    print("Random Values by Weighted Table")
    print(f"{'-' * 73}\n")
    weights = (7, 4, 2, 10, 3, 4)
    cum_weights = (7, 11, 13, 23, 26, 30)
    pop = ("Apple", "Banana", "Cherry", "Grape", "Lime", "Orange")
    distribution_timer(
        random.choices, pop, cum_weights=cum_weights,
        call_sig="Base Case:\nrandom.choices(pop, cum_weights=cum_weights)"
    )
    distribution_timer(
        random.choices, pop, weights,
        call_sig="Base Case:\nrandom.choices(pop, weights)"
    )
    cumulative_table = (
        (7, "Apple"),
        (11, "Banana"),
        (13, "Cherry"),
        (23, "Grape"),
        (26, "Lime"),
        (30, "Orange"),
    )
    cumulative_choice = CumulativeWeightedChoice(cumulative_table)
    distribution_timer(cumulative_choice, call_sig="cumulative_choice()")
    relative_table = (
        (7, "Apple"),
        (4, "Banana"),
        (2, "Cherry"),
        (10, "Grape"),
        (3, "Lime"),
        (4, "Orange"),
    )
    relative_choice = RelativeWeightedChoice(relative_table)
    distribution_timer(relative_choice, call_sig="relative_choice()")
    print("")

    print("Random Values by Key: MultiCat")
    print(f"{'-' * 73}\n")
    multi_cat = MultiCat(
        OrderedDict({
            "Cat_A": ("A1", "A2", "A3", "A4", "A5"),
            "Cat_B": ("B1", "B2", "B3", "B4", "B5"),
            "Cat_C": ("C1", "C2", "C3", "C4", "C5")
        })
    )
    distribution_timer(multi_cat, 'Cat_A', call_sig="multi_cat('Cat_A')")
    distribution_timer(multi_cat, 'Cat_B', call_sig="multi_cat('Cat_B')")
    distribution_timer(multi_cat, 'Cat_C', call_sig="multi_cat('Cat_C')")
    distribution_timer(multi_cat, call_sig="multi_cat()")
    print("")

    r, s = 10, 10
    print(f"Multi Dice: {r}d{s}")
    print(f"{'-' * 73}\n")
    # distribution_timer(randint_dice, r, s, call_sig=f"Base Case:\nrandint_dice({r}, {s})"),
    distribution_timer(randrange_dice, r, s, call_sig=f"Base Case:\nrandrange_dice({r}, {s})"),
    distribution_timer(floor_dice, r, s, call_sig=f"Base Case:\nfloor_dice({r}, {s})"),
    distribution_timer(dice, r, s, call_sig=f"Fortuna.dice({r}, {s})"),
    distribution_timer(fast_dice, r, s, call_sig=f"Fast Base Case:\nFortuna.fast_dice({r}, {s})"),
    print("")

    print(f"{'-' * 73}")
    total_test_time = round((datetime.now() - t0).total_seconds(), 2)
    print(f"Total Test Time: {total_test_time} sec\n")
