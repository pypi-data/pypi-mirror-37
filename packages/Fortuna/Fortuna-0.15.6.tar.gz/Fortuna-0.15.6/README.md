# Fortuna
##### Fast & Flexible Random Value Generator, or Adventures in Non-determinism
Copyright (c) 2018 Broken aka Robert Sharp \
\
\
More than just a high performance random number generator... \
Fortuna can help you build rarefied treasure tables and more.

#### Suggested Installation Method:
- Open your favorite Unix terminal and type `pip install Fortuna`

## Primary Functions

_Note: All ranges are inclusive unless stated otherwise._

`Fortuna.random_range(lo: int, hi: int) -> int` \
Input order is ignored. \
Returns a random integer in range (lo..hi) inclusive. \
Flat uniform distribution.

`Fortuna.random_below(num: int) -> int` \
Returns a random integer in range (0..num-1) for positive values of num. \
Returns a random integer in range (num+1..0) for negative values of num. \
Returns 0 for values of num in range (-1..1) \
Flat uniform distribution.

`Fortuna.d(sides: int) -> int` \
Returns a random integer in the range (1, sides) \
Represents a single die roll. \
Flat uniform distribution.

`Fortuna.dice(rolls: int, sides: int) -> int` \
Returns a random integer in range (rolls..(sides * rolls)) \
Return value represents the sum of multiple rolls of the same dice. \
Geometric distribution based on number and size of the dice rolled. \
Complexity scales with the number of rolls.

`Fortuna.plus_or_minus(num: int) -> int` \
Negative or positive input will produce an equivalent distribution. \
Returns random integer in the range (-num, num) \
Flat uniform distribution.

`Fortuna.plus_or_minus_linear(num: int) -> int` \
Negative or positive input will produce an equivalent distribution. \
Returns random integer in the range (-num, num) \
Zero peak geometric distribution, 45 degree isosceles triangle.

`Fortuna.plus_or_minus_curve(num: int) -> int` \
Negative or positive input will produce an equivalent distribution. \
Returns random integer in the range (-num, num) \
Zero peak gaussian distribution, bell curve.

`Fortuna.percent_true(num: int) -> bool` \
Always returns False if num is 0 or less, always returns True if num is 100 or more. \
Any value of num in range (1..99) will produce True or False. \
Returns a random Bool based on the probability of True as a percentage.

`Fortuna.random_value(arr: sequence) -> value` \
Returns a random value from a sequence (list or tuple), uniform distribution, non-destructive. \
Up to 4x faster than random.choice().

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
Both produce a custom distribution of values based on the weights of the values.

- Constructors take a copy of a 2d sequence of weighted value pairs... `[(weight, value), ... ]`
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
MultiCat is an abstraction layer to enable random selection from a sequence inside an OrderedDict 
by passing an optional category key. MultiCat uses RandomCycle() to produce a uniform  
distribution cycle of values within each cat sequence. If no key is provided - MultiCat will use Mostly() 
to choose a random key for you, where keys at the beginning of the key list are more common than keys at the back.
This makes the top of the data structure geometrically more common than the bottom. \
Cats love to be on top.
<pre>
random_spells = MultiCat(
    OrderedDict({
        "cantrip": ("Acid Splash", "Blade Ward", "Chill Touch", "Dancing Lights", "Fire Bolt"),
        "level_1": ("Burning Hands", "Charm Person", "Chromatic Orb", "Detect Magic", "Find Familiar"),
        "level_2": ("Blindness", "Blur", "Cloud of Daggers", "Continual Flame", "Gust of Wind")
    })
)
random_spells() -> random value from random sequence
random_spells("cantrip") -> random value from "cantrip" sequence
</pre>


## Fortuna 0.15.6 Sample Distribution and Performance Tests
Testbed: MacOS 10.13.6, Python3.7, Skylake 2.7 GHz Intel Core i7, 16GB RAM, 1TB PCIe SSD
<pre>
$ python3.7 .../fortuna_extras/fortuna_tests.py

Running 100,000 cycles of each...


Random Numbers
-------------------------------------------------------------------------

Base Case:
random.randrange(10) x 100000: 101.98 ms
 0: 10.04%
 1: 10.13%
 2: 10.07%
 3: 10.0%
 4: 9.96%
 5: 9.86%
 6: 10.06%
 7: 10.09%
 8: 10.03%
 9: 9.77%

Fortuna.random_below(10) x 100000: 9.71 ms
 0: 10.02%
 1: 9.98%
 2: 10.16%
 3: 9.94%
 4: 9.96%
 5: 9.98%
 6: 9.94%
 7: 10.08%
 8: 9.98%
 9: 9.95%

Base Case:
random.randint(1, 10) x 100000: 147.28 ms
 1: 9.82%
 2: 9.83%
 3: 9.94%
 4: 10.15%
 5: 10.06%
 6: 9.95%
 7: 10.11%
 8: 10.05%
 9: 10.03%
 10: 10.07%

Fortuna.random_range(1, 10) x 100000: 9.89 ms
 1: 9.94%
 2: 9.88%
 3: 9.94%
 4: 10.13%
 5: 10.1%
 6: 10.23%
 7: 9.93%
 8: 10.02%
 9: 9.82%
 10: 10.01%

Fortuna.d(10) x 100000: 9.68 ms
 1: 10.02%
 2: 10.1%
 3: 9.94%
 4: 9.92%
 5: 10.03%
 6: 10.04%
 7: 9.9%
 8: 10.03%
 9: 10.02%
 10: 10.01%

Fortuna.dice(1, 10) x 100000: 9.91 ms
 1: 9.98%
 2: 9.8%
 3: 10.11%
 4: 9.95%
 5: 9.94%
 6: 9.95%
 7: 10.13%
 8: 10.11%
 9: 9.95%
 10: 10.09%

Fortuna.plus_or_minus(5) x 100000: 9.59 ms
 -5: 8.98%
 -4: 9.09%
 -3: 9.02%
 -2: 9.15%
 -1: 9.11%
 0: 9.12%
 1: 9.07%
 2: 9.03%
 3: 9.16%
 4: 9.12%
 5: 9.15%

Fortuna.plus_or_minus_linear(5) x 100000: 12.24 ms
 -5: 2.76%
 -4: 5.59%
 -3: 8.34%
 -2: 10.91%
 -1: 14.11%
 0: 16.6%
 1: 14.02%
 2: 11.08%
 3: 8.31%
 4: 5.51%
 5: 2.76%

Fortuna.plus_or_minus_curve(5) x 100000: 14.99 ms
 -5: 0.22%
 -4: 1.15%
 -3: 4.43%
 -2: 11.45%
 -1: 20.51%
 0: 24.56%
 1: 20.45%
 2: 11.42%
 3: 4.38%
 4: 1.18%
 5: 0.23%


Random Truth
-------------------------------------------------------------------------

Fortuna.percent_true(25) x 100000: 8.82 ms
 False: 74.95%
 True: 25.05%


Random Values from a Sequence
-------------------------------------------------------------------------

some_list = ['Alpha', 'Beta', 'Delta', 'Eta', 'Gamma', 'Kappa', 'Zeta']

Base Case:
random.choice(some_list) x 100000: 79.2 ms
 Alpha: 14.27%
 Beta: 14.18%
 Delta: 14.33%
 Eta: 14.39%
 Gamma: 14.39%
 Kappa: 14.18%
 Zeta: 14.27%

Fortuna.random_value(some_list) x 100000: 13.48 ms
 Alpha: 14.27%
 Beta: 14.3%
 Delta: 14.14%
 Eta: 14.34%
 Gamma: 14.43%
 Kappa: 14.27%
 Zeta: 14.24%

monty = Mostly(some_list)

monty.mostly_front() x 100000: 29.1 ms
 Alpha: 24.91%
 Beta: 21.56%
 Delta: 17.77%
 Eta: 14.21%
 Gamma: 10.7%
 Kappa: 7.35%
 Zeta: 3.51%

monty.mostly_middle() x 100000: 24.74 ms
 Alpha: 6.28%
 Beta: 12.53%
 Delta: 18.73%
 Eta: 24.97%
 Gamma: 18.74%
 Kappa: 12.6%
 Zeta: 6.15%

monty.mostly_back() x 100000: 29.45 ms
 Alpha: 3.56%
 Beta: 7.15%
 Delta: 10.71%
 Eta: 14.34%
 Gamma: 17.79%
 Kappa: 21.52%
 Zeta: 24.93%

monty.mostly_first() x 100000: 32.54 ms
 Alpha: 34.12%
 Beta: 29.97%
 Delta: 20.04%
 Eta: 10.3%
 Gamma: 4.11%
 Kappa: 1.19%
 Zeta: 0.27%

monty.mostly_center() x 100000: 27.64 ms
 Alpha: 0.41%
 Beta: 5.27%
 Delta: 24.11%
 Eta: 40.02%
 Gamma: 24.37%
 Kappa: 5.4%
 Zeta: 0.41%

monty.mostly_last() x 100000: 33.8 ms
 Alpha: 0.29%
 Beta: 1.19%
 Delta: 3.94%
 Eta: 10.38%
 Gamma: 19.78%
 Kappa: 30.25%
 Zeta: 34.17%

monty() x 100000: 48.79 ms
 Alpha: 10.95%
 Beta: 12.93%
 Delta: 16.36%
 Eta: 19.83%
 Gamma: 16.22%
 Kappa: 12.86%
 Zeta: 10.84%

truffle_shuffle = RandomCycle(some_list)

truffle_shuffle() x 100000: 66.29 ms
 Alpha: 14.25%
 Beta: 14.33%
 Delta: 14.25%
 Eta: 14.3%
 Gamma: 14.27%
 Kappa: 14.25%
 Zeta: 14.34%


Random Values by Weighted Table
-------------------------------------------------------------------------

cumulative_table = [(7, "Apple"), (11, "Banana"), (13, "Cherry"), (23, "Grape"), (26, "Lime"), (30, "Orange")]
cumulative_choice = CumulativeWeightedChoice(cumulative_table)

cumulative_choice() x 100000: 27.67 ms
 Apple: 23.3%
 Banana: 13.31%
 Cherry: 6.73%
 Grape: 33.03%
 Lime: 10.02%
 Orange: 13.61%

relative_table = [(7, "Apple"), (4, "Banana"), (2, "Cherry"), (10, "Grape"), (3, "Lime"), (4, "Orange")]
relative_choice = RelativeWeightedChoice(relative_table)

relative_choice() x 100000: 28.58 ms
 Apple: 23.26%
 Banana: 13.33%
 Cherry: 6.66%
 Grape: 33.47%
 Lime: 10.04%
 Orange: 13.24%


MultiCat
-------------------------------------------------------------------------

random_spells('cantrip') x 100000: 79.2 ms
 Acid Splash: 19.93%
 Blade Ward: 20.04%
 Chill Touch: 19.96%
 Dancing Lights: 20.11%
 Fire Bolt: 19.96%

random_spells('level_1') x 100000: 80.35 ms
 Burning Hands: 20.07%
 Charm Person: 19.88%
 Chromatic Orb: 20.14%
 Detect Magic: 19.93%
 Find Familiar: 19.98%

random_spells('level_2') x 100000: 82.74 ms
 Blindness: 20.03%
 Blur: 19.95%
 Cloud of Daggers: 20.02%
 Continual Flame: 20.05%
 Gust of Wind: 19.96%

random_spells() x 100000: 102.39 ms
 Acid Splash: 9.9%
 Blade Ward: 10.0%
 Blindness: 3.38%
 Blur: 3.36%
 Burning Hands: 6.69%
 Charm Person: 6.71%
 Chill Touch: 9.95%
 Chromatic Orb: 6.67%
 Cloud of Daggers: 3.38%
 Continual Flame: 3.36%
 Dancing Lights: 9.96%
 Detect Magic: 6.63%
 Find Familiar: 6.71%
 Fire Bolt: 9.94%
 Gust of Wind: 3.38%


Multi Dice: 10d10
-------------------------------------------------------------------------

Base Case:
randrange_dice(10, 10) x 100000: 968.49 ms

Base Case:
floor_dice(10, 10) x 100000: 275.23 ms

Fortuna.dice(10, 10) x 100000: 38.98 ms


-------------------------------------------------------------------------
Total Test Time: 2.75 sec


Process finished with exit code 0
</pre>

## Change Log

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
Fortuna :: Copyright (c) 2018 Robert Sharp aka Broken

Permission is hereby granted, free of charge, to any person obtaining a copy \
of this software and associated documentation files (the "Software"), to deal \
in the Software without restriction, including without limitation the rights \
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell \
copies of the Software, and to permit persons to whom the Software is \
furnished to do so, subject to the following conditions:

This readme file shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR \
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, \
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE \
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER \
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, \
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE \
SOFTWARE.
