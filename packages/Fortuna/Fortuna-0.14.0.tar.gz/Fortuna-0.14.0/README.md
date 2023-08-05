# Fortuna
##### Fast & Flexible Random Value Generator
Copyright (c) 2018 Robert Sharp


## Primary Functions

`Fortuna.random_range(int A, int B) -> int` \
Returns a random integer within the range (A, B), inclusive uniform distribution. \
Nearly ten times faster than random.randrange() or random.randint().

`Fortuna.d(int sides) -> int` \
Returns a random integer in the range (1, sides), inclusive uniform distribution. \
Represents a single die roll.

`Fortuna.dice(int rolls, int sides) -> int` \
Returns a geometric distribution based on number and size of dice rolled. \
Represents the sum of multiple die rolls.

`Fortuna.plus_or_minus(int N) -> int` \
Returns random integer in the range (-N, N), inclusive uniform distribution.

`Fortuna.plus_or_minus_linear(int N) -> int` \
Returns random integer in the range (-N, N), inclusive zero peak geometric distribution.

`Fortuna.plus_or_minus_curve(int N) -> int` \
Returns random integer in the range (-N, N), inclusive zero peak gaussian distribution.

`Fortuna.percent_true(int N) -> bool` \
Returns a random Bool based on N: the probability of True as a percentage.

`Fortuna.random_value(list) -> value` \
Returns a random value from a list or tuple, non-destructive. Replaces random.choice().

## Abstractions

### Mostly: Random Patterns
- Constructor takes a sequence of unique values.
- Sequence must have 3 or more items, works best with 10 or more.
- Values can be any object, not just strings as in the example below.
- Provides a variety of methods for choosing a random value based on position in the list.
- Performance scales by some tiny fraction of the length of the sequence.
<pre>
some_sequence = ["Alpha", "Beta", "Delta", "Eta", "Gamma", "Kappa", "Zeta"]
random_monty = Fortuna.Mostly(some_sequence)
</pre>
`random_monty.mostly_front() -> value` \
Returns a random value, mostly from the front of the list (geometric)

`random_monty.mostly_middle() -> value` \
Returns a random value, mostly from the middle of the list (geometric)

`random_monty.mostly_back() -> value` \
Returns a random value, mostly from the back of the list (geometric)

`random_monty.mostly_first() -> value` \
Returns a random value, mostly from the very front of the list (gaussian)

`random_monty.mostly_center() -> value` \
Returns a random value, mostly from the very center of the list (gaussian)

`random_monty.mostly_last() -> value` \
Returns a random value, mostly from the very back of the list (gaussian)

`random_monty() -> value` \
Returns a random value, calls a random method above (complex)

### Random Cycle: The Truffle Shuffle variant
- Constructors take a sequence (list or tuple) of unique arbitrary values.
- Sequence must have 3 or more items. Works best with 10 or more.
- Values can be virtually any Python object that can be passed around... string, int, list, function etc.
- Features continuous smart micro-shuffling: The Truffle Shuffle.
- Performance scales by some small fraction of the length of the sequence.
<pre>
some_sequence = ["Alpha", "Beta", "Delta", "Eta", "Gamma", "Kappa", "Zeta"]
random_cycle = Fortuna.RandomCycle(some_sequence)
random_cycle() -> value
</pre>
Returns a random value, produces uniform distributions with no consecutive duplicates
 and relatively few nearby duplicates. This "fuzzy" behavior gives rise to output sequences
 that seem much less mechanical compared to the output of other random_value algorithms.

### Weighted Choice: Custom Rarity
- Constructors will take a 2d sequence (list or tuple) of weighted values... `[(weight, value), ... ]`
- Sequence must not be empty.
- Weights must be integers. 
- Values can be any Python object that can be passed around... string, int, list, function etc.
- Each returns a random value, and produce custom distributions based on weighting.
- Performance scales by some fraction of the length of the sequence.

The following examples produce equivalent distributions with comparable performance. 
The choice to use one over the other is purely about which strategy suits you or the data.
Relative weights are easier to understand at a glance, 

#### Relative Weight Strategy:
<pre>
relative_weighted_table = (
    (7, "Apple"),
    (4, "Banana"),
    (2, "Cherry"),
    (10, "Grape"),
    (3, "Lime"),
    (4, "Orange"),
)
relative_weighted_choice = Fortuna.RelativeWeightedChoice(relative_weighted_table)
relative_weighted_choice() -> value
</pre>

#### Cumulative Weight Strategy:
Note: Logic dictates Cumulative Weights must be unique!
<pre>
cumulative_weighted_table = (
    (7, "Apple"),
    (11, "Banana"),
    (13, "Cherry"),
    (23, "Grape"),
    (26, "Lime"),
    (30, "Orange"),
)
cumulative_weighted_choice = Fortuna.CumulativeWeightedChoice(cumulative_weighted_table)
cumulative_weighted_choice() -> value
</pre>


## Sample Distribution and Performance Test Suite
<pre>
.../fortuna_extras/fortuna_tests.py

Running 100,000 cycles of each...

Random Numbers
------------------------------------------------------------------------

Base Case:
random.randrange(10) x 100000: 150.65 ms
 0: 9.95%
 1: 10.22%
 2: 10.12%
 3: 10.0%
 4: 9.84%
 5: 10.09%
 6: 10.13%
 7: 9.89%
 8: 9.85%
 9: 9.93%

Base Case:
random.randint(1, 10) x 100000: 161.54 ms
 1: 10.2%
 2: 9.93%
 3: 10.0%
 4: 9.99%
 5: 9.96%
 6: 10.06%
 7: 10.02%
 8: 10.0%
 9: 9.98%
 10: 9.85%

random_range(1, 10) x 100000: 10.39 ms
 1: 9.89%
 2: 9.94%
 3: 10.05%
 4: 10.12%
 5: 9.98%
 6: 10.12%
 7: 9.96%
 8: 9.95%
 9: 9.93%
 10: 10.07%

d(6) x 100000: 8.9 ms
 1: 16.75%
 2: 16.66%
 3: 16.69%
 4: 16.69%
 5: 16.66%
 6: 16.56%

dice(2, 6) x 100000: 11.45 ms
 2: 2.71%
 3: 5.53%
 4: 8.29%
 5: 11.13%
 6: 13.9%
 7: 16.65%
 8: 13.84%
 9: 11.22%
 10: 8.36%
 11: 5.61%
 12: 2.77%

plus_or_minus(5) x 100000: 9.07 ms
 -5: 9.32%
 -4: 9.03%
 -3: 9.17%
 -2: 9.03%
 -1: 8.95%
 0: 9.13%
 1: 8.98%
 2: 9.18%
 3: 9.2%
 4: 9.04%
 5: 8.96%

plus_or_minus_linear(5) x 100000: 11.61 ms
 -5: 2.8%
 -4: 5.61%
 -3: 8.34%
 -2: 11.07%
 -1: 14.02%
 0: 16.57%
 1: 13.89%
 2: 11.25%
 3: 8.22%
 4: 5.51%
 5: 2.72%

plus_or_minus_curve(5) x 100000: 13.61 ms
 -5: 0.2%
 -4: 1.1%
 -3: 4.32%
 -2: 11.51%
 -1: 20.42%
 0: 24.81%
 1: 20.18%
 2: 11.69%
 3: 4.44%
 4: 1.13%
 5: 0.2%


Random Truth
------------------------------------------------------------------------

percent_true(25) x 100000: 8.42 ms
 False: 75.02%
 True: 24.98%


Random List Values
------------------------------------------------------------------------

Base Case:
random.choice(some_list) x 100000: 116.49 ms
 Alpha: 14.32%
 Beta: 14.24%
 Delta: 14.5%
 Eta: 14.26%
 Gamma: 14.32%
 Kappa: 14.19%
 Zeta: 14.16%

random_value(some_list) x 100000: 17.9 ms
 Alpha: 14.29%
 Beta: 14.24%
 Delta: 14.21%
 Eta: 14.27%
 Gamma: 14.39%
 Kappa: 14.23%
 Zeta: 14.36%

Mostly.mostly_front() x 100000: 35.7 ms
 Alpha: 24.81%
 Beta: 21.5%
 Delta: 17.98%
 Eta: 14.2%
 Gamma: 10.71%
 Kappa: 7.25%
 Zeta: 3.54%

Mostly.mostly_middle() x 100000: 30.47 ms
 Alpha: 6.35%
 Beta: 12.53%
 Delta: 18.82%
 Eta: 24.8%
 Gamma: 18.78%
 Kappa: 12.4%
 Zeta: 6.32%

Mostly.mostly_back() x 100000: 38.3 ms
 Alpha: 3.58%
 Beta: 7.02%
 Delta: 10.69%
 Eta: 14.1%
 Gamma: 18.11%
 Kappa: 21.39%
 Zeta: 25.11%

Mostly.mostly_first() x 100000: 51.04 ms
 Alpha: 34.44%
 Beta: 29.81%
 Delta: 19.97%
 Eta: 10.33%
 Gamma: 4.03%
 Kappa: 1.16%
 Zeta: 0.27%

Mostly.mostly_center() x 100000: 40.63 ms
 Alpha: 0.41%
 Beta: 5.41%
 Delta: 24.17%
 Eta: 39.98%
 Gamma: 24.14%
 Kappa: 5.44%
 Zeta: 0.45%

Mostly.mostly_last() x 100000: 35.56 ms
 Alpha: 0.28%
 Beta: 1.16%
 Delta: 4.01%
 Eta: 10.34%
 Gamma: 19.97%
 Kappa: 30.03%
 Zeta: 34.21%

Mostly() x 100000: 92.47 ms
 Alpha: 11.03%
 Beta: 12.78%
 Delta: 16.44%
 Eta: 19.64%
 Gamma: 16.37%
 Kappa: 12.94%
 Zeta: 10.81%

RandomCycle() x 100000: 86.44 ms
 Alpha: 14.22%
 Beta: 14.28%
 Delta: 14.31%
 Eta: 14.3%
 Gamma: 14.28%
 Kappa: 14.22%
 Zeta: 14.39%


Random Values by Weight
------------------------------------------------------------------------

RelativeWeightedChoice() x 100000: 31.85 ms
 Apple: 23.41%
 Banana: 13.24%
 Cherry: 6.61%
 Grape: 33.52%
 Lime: 9.95%
 Orange: 13.27%

CumulativeWeightedChoice() x 100000: 31.96 ms
 Apple: 23.47%
 Banana: 13.21%
 Cherry: 6.61%
 Grape: 33.29%
 Lime: 9.99%
 Orange: 13.42%


------------------------------------------------------------------------
Total Test Time: 1.38 sec

Process finished with exit code 0
</pre>

## Update History

#### Fortuna 0.13.3
_Fixed Test Bug: percent sign was missing in output distributions._ \
_Readme updated: added update history, fixed some typos._

#### Fortuna 0.13.2
_Readme updated for even more clarity._

#### Fortuna 0.13.1
_Readme updated for clarity._

#### Fortuna 0.13.0
_Minor Bug Fixes._ \
_Readme updated for aesthetics._ \
_Added Tests: .../fortuna_extras/fortuna_tests.py_

#### Fortuna 0.12.0
_Internal test for future update._

#### Fortuna 0.11.0
_Initial Release: Public Beta_
