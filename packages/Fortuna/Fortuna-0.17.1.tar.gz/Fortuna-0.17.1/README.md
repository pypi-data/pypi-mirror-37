# Fortuna: Fast & Flexible Random Value Generator
#### Adventures in Predictable Non-determinism
More than just a high performance random number generator. 
Fortuna can help you build dynamic rarefied random generators and more. 
See the Treasure Tables in ...fortuna_extras/fortuna_examples.py

#### Suggested Installation Method:
Open your favorite Unix terminal and type `pip install Fortuna`

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


## Class Abstractions
### Quantum Monty: previously Mostly
A set of strategies for producing random values from a sequence where the probability \
of each value is based on the monty you choose. For example: the mostly_front monty \
produces random values where the beginning of the sequence is geometrically more common than the back.

- Constructor takes a copy of a sequence (list or tuple) of arbitrary values.
- Sequence length must be greater than three, best if ten or more.
- Values can be any Python object that can be passed around... string, int, list, function etc.
- Performance scales by some tiny fraction of the length of the sequence. Method scaling may very slightly.
<pre>
some_sequence = ["Alpha", "Beta", "Delta", "Eta", "Gamma", "Kappa", "Zeta"]
quantum_monty = Fortuna.QuantumMonty(some_sequence)
</pre>
`quantum_monty.mostly_front() -> value` \
Returns a random value, mostly from the front of the list (geometric)

`quantum_monty.mostly_middle() -> value` \
Returns a random value, mostly from the middle of the list (geometric)

`quantum_monty.mostly_back() -> value` \
Returns a random value, mostly from the back of the list (geometric)

`quantum_monty.mostly_first() -> value` \
Returns a random value, mostly from the very front of the list (gaussian)

`quantum_monty.mostly_center() -> value` \
Returns a random value, mostly from the very center of the list (gaussian)

`quantum_monty.mostly_last() -> value` \
Returns a random value, mostly from the very back of the list (gaussian)

`quantum_monty.mostly_flat() -> value` \
Returns a random value, (uniform flat)

`quantum_monty.mostly_cycle() -> value` \
Returns a random value, cycles the data with Truffle Shuffle (uniform flat)

`quantum_monty.quantum_monty() -> value` \
Returns a random value, Quantum Monty Algorithm (complex non-uniform)

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

### FlexCat, previously MultiCat
_Controlled Chaos Incarnate_ \
FlexCat wraps an OrderedDict of keyed sequences.
The Y axis keys are accessed directly, or randomized with one of the QuantumMonty methods (y_bias).
The X axis sequences are randomized with one of the QuantumMonty methods (x_bias).

By default FlexCat will use y_bias="front" and x_bias="cycle" if none are specified at initialization. 
This will make the top of the data structure geometrically more common than the bottom and produces a flat 
distribution for each category. With nine methods across two dimensions... that's 81 configurations.

Options for x & y bias: _See QuantumMonty for details_
- front, geometric descending
- middle, geometric pyramid
- back, geometric ascending
- first, gaussian descending
- center, gaussian bell curve
- last, gaussian ascending
- flat, uniform flat
- cycle, cycled uniform flat
- monty, Quantum Monty algorithm

<pre>
flex_cat = FlexCat(
    OrderedDict({
        "Cat_A": ("A1", "A2", "A3", "A4", "A5"),
        "Cat_B": ("B1", "B2", "B3", "B4", "B5"),
        "Cat_C": ("C1", "C2", "C3", "C4", "C5"),
    }), y_bias="cycle", x_bias="cycle"
)
flex_cat("Cat_A") -> random value from "Cat_A" : cycled uniform distribution
flex_cat("Cat_B") -> random value from "Cat_B" : cycled uniform distribution
flex_cat("Cat_C") -> random value from "Cat_C" : cycled uniform distribution
flex_cat() -> random value from randomly cycled category : cycled uniform distribution
</pre>


## Fortuna 0.17.1 Sample Distribution and Performance Tests
Testbed: MacOS 10.13.6, Python3.7, Skylake 2.7 GHz Intel Core i7, 16GB RAM, 1TB PCIe SSD
<pre>
$ python3.7 .../fortuna_extras/fortuna_tests.py

Running 1,000,000 cycles of each...


Random Numbers
-------------------------------------------------------------------------

Base Case:
random.randint(1, 10) x 1000000: 1255.58 ms
 1: 9.98%
 2: 9.99%
 3: 9.99%
 4: 10.04%
 5: 10.01%
 6: 9.95%
 7: 9.99%
 8: 10.02%
 9: 10.0%
 10: 10.02%

Fortuna.random_range(1, 10) x 1000000: 80.79 ms
 1: 9.98%
 2: 10.0%
 3: 10.03%
 4: 10.05%
 5: 10.03%
 6: 10.01%
 7: 9.98%
 8: 9.93%
 9: 9.97%
 10: 10.01%

Base Case:
random.randrange(10) x 1000000: 894.45 ms
 0: 10.0%
 1: 10.01%
 2: 9.97%
 3: 9.99%
 4: 9.98%
 5: 9.99%
 6: 10.02%
 7: 10.01%
 8: 10.05%
 9: 9.97%

Fortuna.random_below(10) x 1000000: 80.75 ms
 0: 10.05%
 1: 10.0%
 2: 10.01%
 3: 9.95%
 4: 10.0%
 5: 10.05%
 6: 10.01%
 7: 10.01%
 8: 9.97%
 9: 9.95%

Fortuna.d(10) x 1000000: 79.05 ms
 1: 9.96%
 2: 10.02%
 3: 10.01%
 4: 9.95%
 5: 10.01%
 6: 10.03%
 7: 9.98%
 8: 10.02%
 9: 10.02%
 10: 10.0%

Fortuna.dice(2, 6) x 1000000: 104.85 ms
 2: 2.81%
 3: 5.53%
 4: 8.29%
 5: 11.16%
 6: 13.85%
 7: 16.7%
 8: 13.86%
 9: 11.13%
 10: 8.33%
 11: 5.54%
 12: 2.81%

Fortuna.plus_or_minus(5) x 1000000: 76.05 ms
 -5: 9.06%
 -4: 9.14%
 -3: 9.07%
 -2: 9.07%
 -1: 9.13%
 0: 9.08%
 1: 9.1%
 2: 9.06%
 3: 9.12%
 4: 9.07%
 5: 9.11%

Fortuna.plus_or_minus_linear(5) x 1000000: 101.32 ms
 -5: 2.77%
 -4: 5.61%
 -3: 8.34%
 -2: 11.07%
 -1: 13.85%
 0: 16.63%
 1: 13.89%
 2: 11.1%
 3: 8.39%
 4: 5.56%
 5: 2.8%

Fortuna.plus_or_minus_curve(5) x 1000000: 125.84 ms
 -5: 0.2%
 -4: 1.16%
 -3: 4.44%
 -2: 11.54%
 -1: 20.35%
 0: 24.67%
 1: 20.39%
 2: 11.48%
 3: 4.42%
 4: 1.14%
 5: 0.2%


Random Truth
-------------------------------------------------------------------------

Fortuna.percent_true(25) x 1000000: 73.19 ms
 False: 74.95%
 True: 25.05%


Random Values from a Sequence
-------------------------------------------------------------------------

Base Case:
random.choice(some_list) x 1000000: 758.83 ms
 Alpha: 14.24%
 Beta: 14.33%
 Delta: 14.28%
 Eta: 14.31%
 Gamma: 14.28%
 Kappa: 14.26%
 Zeta: 14.3%

Fortuna.random_value(some_list) x 1000000: 72.3 ms
 Alpha: 14.23%
 Beta: 14.29%
 Delta: 14.31%
 Eta: 14.31%
 Gamma: 14.37%
 Kappa: 14.27%
 Zeta: 14.22%

monty.mostly_front() x 1000000: 207.48 ms
 Alpha: 24.98%
 Beta: 21.48%
 Delta: 17.84%
 Eta: 14.28%
 Gamma: 10.69%
 Kappa: 7.15%
 Zeta: 3.58%

monty.mostly_middle() x 1000000: 160.06 ms
 Alpha: 6.27%
 Beta: 12.57%
 Delta: 18.72%
 Eta: 24.96%
 Gamma: 18.69%
 Kappa: 12.54%
 Zeta: 6.26%

monty.mostly_back() x 1000000: 206.5 ms
 Alpha: 3.57%
 Beta: 7.12%
 Delta: 10.69%
 Eta: 14.35%
 Gamma: 17.87%
 Kappa: 21.43%
 Zeta: 24.98%

monty.mostly_first() x 1000000: 246.85 ms
 Alpha: 34.24%
 Beta: 30.0%
 Delta: 20.05%
 Eta: 10.21%
 Gamma: 4.01%
 Kappa: 1.21%
 Zeta: 0.27%

monty.mostly_center() x 1000000: 193.77 ms
 Alpha: 0.42%
 Beta: 5.41%
 Delta: 24.19%
 Eta: 39.88%
 Gamma: 24.28%
 Kappa: 5.4%
 Zeta: 0.43%

monty.mostly_last() x 1000000: 248.06 ms
 Alpha: 0.27%
 Beta: 1.22%
 Delta: 4.01%
 Eta: 10.28%
 Gamma: 20.01%
 Kappa: 30.1%
 Zeta: 34.12%

monty.mostly_cycle() x 1000000: 625.13 ms
 Alpha: 14.3%
 Beta: 14.28%
 Delta: 14.29%
 Eta: 14.3%
 Gamma: 14.29%
 Kappa: 14.28%
 Zeta: 14.26%

monty.mostly_flat() x 1000000: 137.62 ms
 Alpha: 14.29%
 Beta: 14.28%
 Delta: 14.28%
 Eta: 14.22%
 Gamma: 14.29%
 Kappa: 14.26%
 Zeta: 14.39%

monty.quantum_monty() x 1000000: 463.61 ms
 Alpha: 11.65%
 Beta: 12.89%
 Delta: 15.88%
 Eta: 19.06%
 Gamma: 15.93%
 Kappa: 12.91%
 Zeta: 11.67%

random_cycle() x 1000000: 550.79 ms
 Alpha: 14.27%
 Beta: 14.25%
 Delta: 14.29%
 Eta: 14.31%
 Gamma: 14.29%
 Kappa: 14.28%
 Zeta: 14.31%


Random Values by Weighted Table
-------------------------------------------------------------------------

Cumulative Base Case:
random.choices(pop, cum_weights=cum_weights) x 1000000: 1931.41 ms
 Apple: 23.35%
 Banana: 13.33%
 Cherry: 6.64%
 Grape: 33.33%
 Lime: 9.99%
 Orange: 13.36%

Relative Base Case:
random.choices(pop, weights) x 1000000: 2275.44 ms
 Apple: 23.31%
 Banana: 13.39%
 Cherry: 6.69%
 Grape: 33.26%
 Lime: 10.0%
 Orange: 13.35%

Fortuna.cumulative_weighted_choice(cumulative_table) x 1000000: 156.84 ms
 Apple: 23.3%
 Banana: 13.37%
 Cherry: 6.67%
 Grape: 33.28%
 Lime: 10.05%
 Orange: 13.33%

cumulative_choice() x 1000000: 259.18 ms
 Apple: 23.39%
 Banana: 13.32%
 Cherry: 6.7%
 Grape: 33.27%
 Lime: 9.97%
 Orange: 13.36%

relative_choice() x 1000000: 259.89 ms
 Apple: 23.37%
 Banana: 13.31%
 Cherry: 6.65%
 Grape: 33.29%
 Lime: 10.0%
 Orange: 13.38%


Random Values by Category
-------------------------------------------------------------------------

flex_cat('Cat_A') x 1000000: 280.97 ms
 A1: 19.98%
 A2: 20.06%
 A3: 19.96%
 A4: 19.99%
 A5: 20.03%

flex_cat('Cat_B') x 1000000: 304.01 ms
 B1: 19.94%
 B2: 20.05%
 B3: 20.05%
 B4: 20.04%
 B5: 19.92%

flex_cat('Cat_C') x 1000000: 322.15 ms
 C1: 20.03%
 C2: 20.04%
 C3: 19.98%
 C4: 19.98%
 C5: 19.97%

flex_cat() x 1000000: 425.07 ms
 A1: 10.04%
 A2: 9.97%
 A3: 9.94%
 A4: 10.05%
 A5: 9.97%
 B1: 6.62%
 B2: 6.72%
 B3: 6.67%
 B4: 6.63%
 B5: 6.7%
 C1: 3.32%
 C2: 3.33%
 C3: 3.32%
 C4: 3.34%
 C5: 3.37%


-------------------------------------------------------------------------
Total Test Time: 17.13 sec


Process finished with exit code 0
</pre>

## Fortuna Beta Development Log
**Fortuna 0.17.1** \
_Fixed some minor typos._

**Fortuna 0.17.0** \
_Added QuantumMonty to replace Mostly, same default behavior with more options._ \
_Mostly is depreciated and may be removed in a future release._ \
_Added FlexCat to replace MultiCat, same default behavior with more options._ \
_MultiCat is depreciated and may be removed in a future release._ \
_Expanded the Treasure Table example in .../fortuna_extras/fortuna_examples.py_

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
