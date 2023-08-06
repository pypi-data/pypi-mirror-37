# Fortuna: Fast & Flexible Random Value Generator
#### Adventures in Predictable Non-determinism
More than just a high performance random number generator. 
Fortuna can help you build dynamic rarefied random generators and more. 
See the MagicItemTable example in fortuna_examples.

#### Suggested Installation Method:
- Open your favorite Unix terminal and type `pip install Fortuna`

## Primary Functions
_Note: All ranges are inclusive unless stated otherwise._

`Fortuna.random_range(lo: int, hi: int) -> int` \
Input order is ignored. \
Returns a random integer in range (lo..hi) inclusive. \
Up to 15x faster than random.randint(). \
Flat uniform distribution.

`Fortuna.random_below(num: int) -> int` \
Returns a random integer in range (0..num-1) for positive values of num. \
Returns a random integer in range (num+1..0) for negative values of num. \
Returns 0 for values of num in range (-1..1) \
Up to 10x faster than random.randrange(). \
Flat uniform distribution.

`Fortuna.d(sides: int) -> int` \
Returns a random integer in the range (1, sides) \
Represents a single die roll of a given size. \
Flat uniform distribution.

`Fortuna.dice(rolls: int, sides: int) -> int` \
Returns a random integer in range (rolls..(sides * rolls)) \
Represents the sum of multiple rolls of the same size die. \
Geometric distribution based on number and size of the dice rolled. \
Complexity scales primarily with the number of rolls.

`Fortuna.plus_or_minus(num: int) -> int` \
Negative or positive input will produce an equivalent distribution. \
Returns random integer in the range (-num, num) \
Flat uniform distribution.

`Fortuna.plus_or_minus_linear(num: int) -> int` \
Negative or positive input will produce an equivalent distribution. \
Returns random integer in the range (-num, num) \
Zero peak geometric distribution, triangle.

`Fortuna.plus_or_minus_curve(num: int) -> int` \
Negative or positive input will produce an equivalent distributions. \
Returns random integer in the range (-num, num) \
Zero peak gaussian distribution, bell curve: Mean = 0, Variance = num / pi

`Fortuna.percent_true(num: int) -> bool` \
Always returns False if num is 0 or less, always returns True if num is 100 or more. \
Any value of num in range (1..99) will produce True or False. \
Returns a random Bool based on the probability of True as a percentage.

`Fortuna.random_value(arr: sequence) -> value` \
Returns a random value from a sequence (list or tuple), uniform distribution, non-destructive. \
Up to 10x faster than random.choice().

`Fortuna.cumulative_weighted_choice(table: sequence) -> value` \
Core function for WeightedChoice base class. \
Produces a custom distribution of values based on cumulative weight. \
Up to 10x to 15x faster than random.choices().


## Fast Base Cases, for testing purposes only.
- Core implementation: c-style random `rand() % N` not recommended!
- These functions may produce distributions with unwanted bias on some platforms.

`Fortuna.fast_d(sides: int) -> int` \
Assumes sides is a positive number > 0 \
Returns a random integer in range (1..sides)

`Fortuna.fast_dice(rolls: int, sides: int) -> int` \
Assumes rolls and sides are a positive numbers > 0 \
Returns a random integer in range (rolls..(sides * rolls)) \
Return value represents the sum of multiple rolls of the same dice.

## Class Abstractions
### Mostly: The Quantum Monty
A set of strategies for producing random values from a sequence where the probability \
of each value is based on it's position in the sequence. For example: the mostly front monty \
produces random values where the beginning of the sequence is geometrically more common than the back.

- Constructor takes a copy of a sequence (list or tuple) of arbitrary values.
- Sequence length must be greater than three, best if ten or more.
- Values can be any Python object that can be passed around... string, int, list, function etc.
- Performance scales by some tiny fraction of the length of the sequence. Method scaling may very slightly.
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
Returns a random value, Quantum Monty Algorithm (complex)

### Random Cycle: The Truffle Shuffle
Returns a random value from the sequence. Produces a uniform distribution with no consecutive duplicates 
and relatively few nearly consecutive duplicates. Longer sequences will naturally push duplicates even further apart. 
This behavior gives rise to output sequences that seem much less mechanical than other random_value sequences. 

- Constructor takes a copy of a sequence (list or tuple) of arbitrary values.
- Sequence length must be greater than three, best if ten or more.
- Values can be any Python object that can be passed around... string, int, list, function etc.
- Features continuous smart micro-shuffling: The Truffle Shuffle.
- Performance scales by some small fraction of the length of the sequence.
<pre>
some_sequence = ["Alpha", "Beta", "Delta", "Eta", "Gamma", "Kappa", "Zeta"]
random_cycle = Fortuna.RandomCycle(some_sequence)
random_cycle() -> value
</pre>

### Weighted Choice: Custom Rarity
Two strategies for selecting random values from a sequence where rarity counts. \
Both produce a custom distribution of values based on the weights of the values. \
Up to 10x faster than random.choices()

- Constructor takes a copy of a sequence of weighted value pairs... `[(weight, value), ... ]`
- The sequence must not be empty, and each pair must have a weight and a value.
- Weights must be integers. A future release may allow weights to be floats.
- Values can be any Python object that can be passed around... string, int, list, function etc.
- Performance scales by some fraction of the length of the sequence.

The following examples produce equivalent distributions with comparable performance. 
The choice to use one over the other is purely about which strategy suits you or the data best.
Relative weights are easier to understand at a glance, while RPG Treasure Tables map rather nicely to cumulative weights.
Cumulative weights are slightly easier for humans to get wrong, because math. Relative weights can be compared directly
while cumulative weights can not. The tables below have been constructed to have the exact same 
probabilities for each corresponding value.

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

### MultiCat
_Controlled chaos incarnate._ \
MultiCat wraps an OrderedDict of keyed sequences. \
The Y axis keys are accessed directly, or randomized with Mostly.mostly_front(). \
The X axis sequences are randomized with RandomCycle() aka the Truffle Shuffle.

If an unrecognized key is passed an exception is thrown.

The top of the data structure is geometrically more common than the bottom when you invoke a 
MultiCat instance without a key. This holds if the sequences are very close to equal length. 
Relative differences in sequence length will also contribute to the over-all probability of values in a super group. 
Values in larger sequences will naturally be more rare than those in shorter sequences.

<pre>
multi_cat = MultiCat(
    OrderedDict({
        "Cat_A": ("A1", "A2", "A3", "A4", "A5"),
        "Cat_B": ("B1", "B2", "B3", "B4", "B5"),
        "Cat_C": ("C1", "C2", "C3", "C4", "C5")
    })
)
multi_cat("Cat_A") -> random value from "Cat_A" : uniform distribution
multi_cat("Cat_B") -> random value from "Cat_B" : uniform distribution
multi_cat("Cat_C") -> random value from "Cat_C" : uniform distribution
multi_cat() -> random value from random category: linear descending platues
</pre>


## Fortuna 0.16.2 Sample Distribution and Performance Tests
Testbed: MacOS 10.13.6, Python3.7, Skylake 2.7 GHz Intel Core i7, 16GB RAM, 1TB PCIe SSD
<pre>
$ python3.7 .../fortuna_extras/fortuna_tests.py

Running 1,000,000 cycles of each...


Random Numbers
-------------------------------------------------------------------------

Base Case:
random.randint(1, 10) x 1000000: 1274.5 ms
 1: 9.98%
 2: 10.02%
 3: 9.98%
 4: 10.0%
 5: 10.02%
 6: 10.04%
 7: 10.03%
 8: 9.99%
 9: 9.97%
 10: 9.96%

Fortuna.random_range(1, 10) x 1000000: 81.9 ms
 1: 10.02%
 2: 10.04%
 3: 9.98%
 4: 10.02%
 5: 10.01%
 6: 9.98%
 7: 10.03%
 8: 10.0%
 9: 9.96%
 10: 9.96%

Base Case:
random.randrange(10) x 1000000: 922.65 ms
 0: 10.01%
 1: 9.96%
 2: 10.0%
 3: 10.03%
 4: 9.97%
 5: 10.04%
 6: 10.02%
 7: 10.03%
 8: 9.98%
 9: 9.96%

Fortuna.random_below(10) x 1000000: 80.23 ms
 0: 10.02%
 1: 10.0%
 2: 10.0%
 3: 9.96%
 4: 10.01%
 5: 10.0%
 6: 10.03%
 7: 10.03%
 8: 9.95%
 9: 10.02%

Fast Base Case:
Fortuna.fast_rand_below(10) x 1000000: 54.07 ms
 0: 9.98%
 1: 10.07%
 2: 10.01%
 3: 10.03%
 4: 9.99%
 5: 10.02%
 6: 9.95%
 7: 9.99%
 8: 9.95%
 9: 10.01%

Fortuna.d(10) x 1000000: 78.59 ms
 1: 9.95%
 2: 10.03%
 3: 10.05%
 4: 10.0%
 5: 10.0%
 6: 10.04%
 7: 9.97%
 8: 9.98%
 9: 10.02%
 10: 9.95%

Fast Base Case:
Fortuna.fast_d(10) x 1000000: 54.9 ms
 1: 10.01%
 2: 9.97%
 3: 9.99%
 4: 9.97%
 5: 10.0%
 6: 10.08%
 7: 10.04%
 8: 9.94%
 9: 10.0%
 10: 10.0%

Fortuna.dice(1, 10) x 1000000: 83.16 ms
 1: 10.0%
 2: 10.02%
 3: 9.99%
 4: 10.1%
 5: 9.96%
 6: 9.91%
 7: 10.0%
 8: 9.99%
 9: 10.03%
 10: 10.0%

Fast Base Case:
Fortuna.fast_dice(1, 10) x 1000000: 56.04 ms
 1: 10.0%
 2: 10.01%
 3: 9.98%
 4: 9.96%
 5: 9.98%
 6: 10.01%
 7: 10.0%
 8: 10.04%
 9: 10.02%
 10: 10.01%

Fortuna.plus_or_minus(5) x 1000000: 75.86 ms
 -5: 9.12%
 -4: 9.14%
 -3: 9.05%
 -2: 9.12%
 -1: 9.09%
 0: 9.06%
 1: 9.08%
 2: 9.1%
 3: 9.1%
 4: 9.11%
 5: 9.05%

Fortuna.plus_or_minus_linear(5) x 1000000: 102.17 ms
 -5: 2.78%
 -4: 5.52%
 -3: 8.31%
 -2: 11.13%
 -1: 13.89%
 0: 16.71%
 1: 13.95%
 2: 11.09%
 3: 8.31%
 4: 5.56%
 5: 2.77%

Fortuna.plus_or_minus_curve(5) x 1000000: 124.75 ms
 -5: 0.2%
 -4: 1.17%
 -3: 4.4%
 -2: 11.5%
 -1: 20.36%
 0: 24.67%
 1: 20.38%
 2: 11.51%
 3: 4.44%
 4: 1.16%
 5: 0.21%


Random Truth
-------------------------------------------------------------------------

Fortuna.percent_true(25) x 1000000: 72.63 ms
 False: 75.05%
 True: 24.95%


Random Values from a Sequence
-------------------------------------------------------------------------

Base Case:
random.choice(some_list) x 1000000: 766.71 ms
 Alpha: 14.32%
 Beta: 14.24%
 Delta: 14.25%
 Eta: 14.28%
 Gamma: 14.31%
 Kappa: 14.28%
 Zeta: 14.32%

Fortuna.random_value(some_list) x 1000000: 76.98 ms
 Alpha: 14.32%
 Beta: 14.23%
 Delta: 14.29%
 Eta: 14.33%
 Gamma: 14.28%
 Kappa: 14.33%
 Zeta: 14.23%

mostly.mostly_front() x 1000000: 212.36 ms
 Alpha: 24.99%
 Beta: 21.46%
 Delta: 17.77%
 Eta: 14.3%
 Gamma: 10.71%
 Kappa: 7.17%
 Zeta: 3.59%

mostly.mostly_middle() x 1000000: 165.0 ms
 Alpha: 6.22%
 Beta: 12.54%
 Delta: 18.75%
 Eta: 24.93%
 Gamma: 18.75%
 Kappa: 12.55%
 Zeta: 6.25%

mostly.mostly_back() x 1000000: 210.55 ms
 Alpha: 3.58%
 Beta: 7.16%
 Delta: 10.74%
 Eta: 14.33%
 Gamma: 17.8%
 Kappa: 21.42%
 Zeta: 24.98%

mostly.mostly_first() x 1000000: 253.58 ms
 Alpha: 34.31%
 Beta: 29.92%
 Delta: 20.05%
 Eta: 10.23%
 Gamma: 4.0%
 Kappa: 1.2%
 Zeta: 0.28%

mostly.mostly_center() x 1000000: 198.4 ms
 Alpha: 0.43%
 Beta: 5.35%
 Delta: 24.28%
 Eta: 39.97%
 Gamma: 24.19%
 Kappa: 5.35%
 Zeta: 0.43%

mostly.mostly_last() x 1000000: 252.24 ms
 Alpha: 0.27%
 Beta: 1.2%
 Delta: 4.02%
 Eta: 10.25%
 Gamma: 20.11%
 Kappa: 29.97%
 Zeta: 34.17%

mostly() x 1000000: 349.35 ms
 Alpha: 10.91%
 Beta: 12.85%
 Delta: 16.36%
 Eta: 19.85%
 Gamma: 16.34%
 Kappa: 12.84%
 Zeta: 10.86%

random_cycle() x 1000000: 570.53 ms
 Alpha: 14.29%
 Beta: 14.28%
 Delta: 14.28%
 Eta: 14.29%
 Gamma: 14.28%
 Kappa: 14.27%
 Zeta: 14.31%


Random Values by Weighted Table
-------------------------------------------------------------------------

Base Case:
random.choices(pop, cum_weights=cum_weights) x 1000000: 1833.22 ms
 Apple: 23.41%
 Banana: 13.29%
 Cherry: 6.7%
 Grape: 33.3%
 Lime: 10.04%
 Orange: 13.26%

Base Case:
random.choices(pop, weights) x 1000000: 2280.01 ms
 Apple: 23.34%
 Banana: 13.39%
 Cherry: 6.66%
 Grape: 33.27%
 Lime: 9.98%
 Orange: 13.36%

cumulative_choice() x 1000000: 240.53 ms
 Apple: 23.32%
 Banana: 13.37%
 Cherry: 6.69%
 Grape: 33.29%
 Lime: 9.96%
 Orange: 13.37%

relative_choice() x 1000000: 242.73 ms
 Apple: 23.28%
 Banana: 13.34%
 Cherry: 6.67%
 Grape: 33.36%
 Lime: 10.02%
 Orange: 13.33%


Random Values by Key: MultiCat
-------------------------------------------------------------------------

multi_cat('Cat_A') x 1000000: 688.4 ms
 A1: 19.99%
 A2: 19.99%
 A3: 20.02%
 A4: 19.98%
 A5: 20.02%

multi_cat('Cat_B') x 1000000: 710.9 ms
 B1: 19.99%
 B2: 19.99%
 B3: 19.99%
 B4: 20.01%
 B5: 20.02%

multi_cat('Cat_C') x 1000000: 739.03 ms
 C1: 20.0%
 C2: 20.02%
 C3: 19.98%
 C4: 20.01%
 C5: 19.99%

multi_cat() x 1000000: 866.33 ms
 A1: 9.97%
 A2: 10.0%
 A3: 9.99%
 A4: 9.99%
 A5: 9.99%
 B1: 6.67%
 B2: 6.67%
 B3: 6.65%
 B4: 6.68%
 B5: 6.68%
 C1: 3.34%
 C2: 3.34%
 C3: 3.34%
 C4: 3.35%
 C5: 3.34%


Multi Dice: 10d10
-------------------------------------------------------------------------

Base Case:
randrange_dice(10, 10) x 1000000: 9847.03 ms

Base Case:
floor_dice(10, 10) x 1000000: 2717.53 ms

Fortuna.dice(10, 10) x 1000000: 383.39 ms

Fast Base Case:
Fortuna.fast_dice(10, 10) x 1000000: 119.82 ms


-------------------------------------------------------------------------
Total Test Time: 31.11 sec


Process finished with exit code 0
</pre>

## Change Log
**Fortuna 0.16.2** \
_Minor refactoring for WeightedChoice_

**Fortuna 0.16.1** \
_Redesigned fortuna_examples.py to feature a dynamic random magic item generator._ \
_Raised cumulative_weighted_choice function to top level._ \
_Added test for cumulative_weighted_choice as free function._ \
_Updated MultiCat documentation for clarity._

**Fortuna 0.16.0** \
_Pushed distribution_timer to the .pyx layer._ \
_Changed default number of iterations of tests to 1 million, up form 1 hundred thousand._ \
_Reordered tests to better match documentation._ \
_Added Base Case Fortuna.fast_rand_below._
_Added Base Case Fortuna.fast_d._ \
_Added Base Case Fortuna.fast_dice._

**Fortuna 0.15.10** \
_Internal Development Cycle_

**Fortuna 0.15.9** \
_Added Base Cases for random.choices_ \
_Added Base Case for randint_dice_

**Fortuna 0.15.8** \
_Clarified MultiCat Test_

**Fortuna 0.15.7** \
_Fixed minor typos._

**Fortuna 0.15.6** \
_Fixed minor typos._ \
_Simplified MultiCat example._

**Fortuna 0.15.5** \
_Added MultiCat test._ \
_Fixed some minor typos in docs._

**Fortuna 0.15.4** \
_Performance optimization for both WeightedChoice() variants._ \
_Cython update provides small performance enhancement across the board._ \
_Compilation now leverages Python3 all the way down._ \
_MultiCat pushed to the .pyx layer for better performance._

**Fortuna 0.15.3** \
_Reworked the MultiCat example to include several randomizing strategies working in concert._ \
_Added Multi Dice 10d10 performance tests._ \
_Updated sudo code in documentation to be more pythonic._

**Fortuna 0.15.2** \
_Fixed: Linux installation failure._ \
_Added: complete source files to the distribution (.cpp .hpp .pyx)._

**Fortuna 0.15.1** \
_Updated & simplified distribution_timer in fortuna_tests.py_ \
_Readme updated, fixed some typos._ \
_Known issue preventing successful installation on some linux platforms._

**Fortuna 0.15.0** \
_Performance tweaks._ \ 
_Readme updated, added some details._

**Fortuna 0.14.1** \
_Readme updated, fixed some typos._

**Fortuna 0.14.0** \
_Fixed a bug where the analytic continuation algorithm caused a rare issue during compilation on some platforms._

**Fortuna 0.13.3** \
_Fixed Test Bug: percent sign was missing in output distributions._ \
_Readme updated: added update history, fixed some typos._

**Fortuna 0.13.2** \
_Readme updated for even more clarity._

**Fortuna 0.13.1** \
_Readme updated for clarity._

**Fortuna 0.13.0** \
_Minor Bug Fixes._ \
_Readme updated for aesthetics._ \
_Added Tests: .../fortuna_extras/fortuna_tests.py_

**Fortuna 0.12.0** \
_Internal test for future update._

**Fortuna 0.11.0** \
_Initial Release: Public Beta_

**Fortuna 0.10.0** \
_Module name changed from Dice to Fortuna_


## Legal Stuff
Fortuna :: Copyright (c) 2018 Broken aka Robert W. Sharp

Permission is hereby granted, free of charge, to any person obtaining a copy \
of this software and associated documentation files (the "Software"), to deal \
in the Software without restriction, including without limitation the rights \
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell \
copies of the Software, and to permit persons to whom the Software is \
furnished to do so, subject to the following conditions:

This README.md file shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR \
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, \
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE \
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER \
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, \
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE \
SOFTWARE.
