# Fortuna
##### Fast & Flexible Random Value Generator, or Adventures in Non-determinism
Copyright (c) 2018 Robert Sharp aka Broken \
\
\
More than just a high performance random number generator... \
Fortuna can help you build rarefied treasure tables and more. \
Examples coming soon.

#### Suggested Installation Method:
- Open your favorite Unix terminal and type `pip install Fortuna`

#### Alternate Installation Method: Install Fortuna from Source Code
- _Building Fortuna Requires: Python3 Dev Tools, a fair bit of knowledge, some goddess magic, and a C++17 64bit compiler._
- Download source files form [pypi.org/project/Fortuna/#files][url], decompress archive.
- Open your favorite Unix terminal, cd to the directory.
- type `python3 setup.py install` then do a quick ritual to honor Falkore the Luck Dragon (optional).
- Assuming that worked... that's it! From Python `import Fortuna` and she's ready to roll your dice.

[url]: https://pypi.org/project/Fortuna/#files

## Primary Functions

`Fortuna.random_range(int A, int B) -> int` \
Features the 64bit Mersenne Twister Algorithm. \
Returns a random integer within the range (A, B), inclusive uniform distribution. \
Ten to fifteen times faster than random.randrange() or random.randint().

`Fortuna.d(int sides) -> int` \
Expects positive input, negative numbers are treated as zero. \
Returns a random integer in the range (1, sides), inclusive uniform distribution. \
Represents a single die roll.

`Fortuna.dice(int rolls, int sides) -> int` \
Expects positive input, negative numbers are treated as zero. \
Output limited to INT_MAX, rolls x sides must be <= 2,147,483,647. \
Returns a geometric distribution based on number and size of dice rolled. \
Represents the sum of multiple die rolls. \
Complexity scales with number of dice rolls.

`Fortuna.plus_or_minus(int N) -> int` \
Returns random integer in the range (-N, N), inclusive uniform distribution.

`Fortuna.plus_or_minus_linear(int N) -> int` \
Returns random integer in the range (-N, N), inclusive zero peak geometric distribution.

`Fortuna.plus_or_minus_curve(int N) -> int` \
Returns random integer in the range (-N, N), inclusive zero peak gaussian distribution.

`Fortuna.percent_true(int N) -> bool` \
Expected input range: 0..100, N=zero always returns False, N=100 always returns True. \
Returns a random Bool based on N: the probability of True as a percentage.

`Fortuna.random_value(list) -> value` \
Returns a random value from a sequence (list or tuple), uniform distribution, non-destructive. \
Replaces random.choice().

## Class Abstractions

### Mostly: The Quantum Monty
- Constructor takes a sequence (list or tuple) of arbitrary values.
- Sequence must have 3 or more items, works best with 10 or more.
- Values can be any Python object that can be passed around... string, int, list, function etc.
- Provides a variety of methods for choosing a random value based on position in the sequence.
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
Returns a random value, Quantum Monty Algorithm (complex overlapped probability waves)

### Random Cycle: The Truffle Shuffle
- Constructor takes a sequence (list or tuple) of arbitrary values.
- Sequence must have 3 or more items. Works best with 10 or more.
- Values can be any Python object that can be passed around... string, int, list, function etc.
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
- Constructors take a 2d sequence (list or tuple) of weighted values... `[(weight, value), ... ]`
- Sequence must not be empty.
- Weights must be integers. 
- Values can be any Python object that can be passed around... string, int, list, function etc.
- Returns a random value, and will produces custom distribution based on weighting.
- Performance scales by some fraction of the length of the sequence.

The following examples produce equivalent distributions with comparable performance. 
The choice to use one over the other is purely about which strategy suits you or the data best.
Relative weights are easier to understand at a glance, while RPG Treasure Tables map nicely to cumulative weights.

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


## Fortuna 0.15.0 Sample Distribution and Performance Test Suite
<pre>
/usr/local/bin/python3.7 .../fortuna_extras/fortuna_tests.py

Running 100,000 cycles of each...

Fortuna 0.15 Sample Distribution and Performance Test Suite

Random Numbers
-------------------------------------------------------------------------

Base Case:
random.randrange(10) x 100000: 107.02 ms
 0: 9.91%
 1: 9.96%
 2: 9.96%
 3: 9.9%
 4: 10.08%
 5: 10.1%
 6: 10.17%
 7: 9.89%
 8: 10.07%
 9: 9.96%

Base Case:
random.randint(1, 10) x 100000: 132.15 ms
 1: 10.01%
 2: 10.09%
 3: 10.04%
 4: 9.94%
 5: 10.05%
 6: 9.9%
 7: 9.99%
 8: 9.93%
 9: 10.08%
 10: 9.98%

random_range(1, 10) x 100000: 9.48 ms
 1: 10.04%
 2: 9.98%
 3: 10.01%
 4: 9.98%
 5: 10.06%
 6: 10.06%
 7: 10.0%
 8: 9.95%
 9: 9.92%
 10: 10.0%

d(6) x 100000: 8.7 ms
 1: 16.51%
 2: 16.79%
 3: 16.68%
 4: 16.56%
 5: 16.76%
 6: 16.7%

dice(2, 6) x 100000: 11.52 ms
 2: 2.8%
 3: 5.52%
 4: 8.24%
 5: 11.22%
 6: 13.95%
 7: 16.4%
 8: 14.04%
 9: 11.14%
 10: 8.33%
 11: 5.56%
 12: 2.8%

plus_or_minus(5) x 100000: 9.55 ms
 -5: 9.14%
 -4: 9.23%
 -3: 9.11%
 -2: 9.17%
 -1: 9.08%
 0: 9.08%
 1: 8.94%
 2: 9.11%
 3: 8.98%
 4: 9.09%
 5: 9.06%

plus_or_minus_linear(5) x 100000: 11.78 ms
 -5: 2.73%
 -4: 5.52%
 -3: 8.46%
 -2: 11.25%
 -1: 13.69%
 0: 16.72%
 1: 13.9%
 2: 11.1%
 3: 8.25%
 4: 5.5%
 5: 2.89%

plus_or_minus_curve(5) x 100000: 13.8 ms
 -5: 0.21%
 -4: 1.15%
 -3: 4.48%
 -2: 11.48%
 -1: 20.3%
 0: 24.7%
 1: 20.54%
 2: 11.37%
 3: 4.45%
 4: 1.1%
 5: 0.21%


Random Truthy
-------------------------------------------------------------------------

percent_true(25) x 100000: 8.49 ms
 False: 74.99%
 True: 25.01%


Random List Values
-------------------------------------------------------------------------

Base Case:
random.choice(some_list) x 100000: 93.81 ms
 Alpha: 14.29%
 Beta: 14.13%
 Delta: 14.48%
 Eta: 14.2%
 Gamma: 14.3%
 Kappa: 14.28%
 Zeta: 14.32%

random_value(some_list) x 100000: 17.38 ms
 Alpha: 14.29%
 Beta: 14.24%
 Delta: 14.26%
 Eta: 14.32%
 Gamma: 14.48%
 Kappa: 14.05%
 Zeta: 14.36%

Mostly.mostly_front() x 100000: 31.6 ms
 Alpha: 25.17%
 Beta: 21.33%
 Delta: 17.8%
 Eta: 14.41%
 Gamma: 10.73%
 Kappa: 7.08%
 Zeta: 3.48%

Mostly.mostly_middle() x 100000: 24.82 ms
 Alpha: 6.3%
 Beta: 12.52%
 Delta: 18.37%
 Eta: 25.01%
 Gamma: 18.88%
 Kappa: 12.65%
 Zeta: 6.27%

Mostly.mostly_back() x 100000: 29.62 ms
 Alpha: 3.65%
 Beta: 7.12%
 Delta: 10.67%
 Eta: 14.24%
 Gamma: 17.82%
 Kappa: 21.76%
 Zeta: 24.74%

Mostly.mostly_first() x 100000: 32.81 ms
 Alpha: 34.3%
 Beta: 29.8%
 Delta: 20.05%
 Eta: 10.33%
 Gamma: 4.05%
 Kappa: 1.16%
 Zeta: 0.3%

Mostly.mostly_center() x 100000: 33.28 ms
 Alpha: 0.42%
 Beta: 5.29%
 Delta: 24.14%
 Eta: 40.12%
 Gamma: 24.09%
 Kappa: 5.5%
 Zeta: 0.43%

Mostly.mostly_last() x 100000: 41.89 ms
 Alpha: 0.3%
 Beta: 1.21%
 Delta: 4.05%
 Eta: 10.28%
 Gamma: 20.1%
 Kappa: 29.67%
 Zeta: 34.38%

Mostly() x 100000: 52.55 ms
 Alpha: 10.78%
 Beta: 12.87%
 Delta: 16.5%
 Eta: 19.87%
 Gamma: 16.37%
 Kappa: 12.79%
 Zeta: 10.82%

RandomCycle() x 100000: 74.27 ms
 Alpha: 14.29%
 Beta: 14.3%
 Delta: 14.17%
 Eta: 14.26%
 Gamma: 14.26%
 Kappa: 14.38%
 Zeta: 14.34%


Random Values by Weighted Table
-------------------------------------------------------------------------

CumulativeWeightedChoice() x 100000: 37.34 ms
 Apple: 23.2%
 Banana: 13.22%
 Cherry: 6.69%
 Grape: 33.46%
 Lime: 10.11%
 Orange: 13.33%

RelativeWeightedChoice() x 100000: 33.07 ms
 Apple: 23.21%
 Banana: 13.3%
 Cherry: 6.73%
 Grape: 33.52%
 Lime: 9.91%
 Orange: 13.33%


-------------------------------------------------------------------------
Total Test Time: 1.1 sec

Process finished with exit code 0

</pre>

## Update History

#### Fortuna 0.15.1
_Updated & simplified distribution_timer in fortuna_tests.py_ \
_Readme updated, fixed some typos._ \
_Known issue preventing successful installation on some linux platforms._

#### Fortuna 0.15.0
_Minor performance tweaks._ \ 
_Readme updated, added some details._

#### Fortuna 0.14.1
_Readme updated, fixed some typos._

#### Fortuna 0.14.0
_Fortuna now requires Python 3.7_ \
_Fixed a bug where the analytic continuation algorithm caused a rare issue during compilation on some platforms._

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


## Legal Stuff
Fortuna :: Copyright (c) 2018 Robert Sharp aka Broken

Permission is hereby granted, free of charge, to any person obtaining a copy \
of this software and associated documentation files (the "Software"), to deal \
in the Software without restriction, including without limitation the rights \
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell \
copies of the Software, and to permit persons to whom the Software is \
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all \
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR \
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, \
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE \
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER \
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, \
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE \
SOFTWARE.
