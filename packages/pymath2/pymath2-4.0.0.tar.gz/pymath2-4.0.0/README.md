# pymath

Perform math calculations either on the command line or in the Python repl.
Imports the following functions/classes/variables into the global namespace for convenience:

- everything from [math](https://docs.python.org/3/library/math.html)
- everything from [statistics](https://docs.python.org/3/library/statistics.html)
- the combinatoric functions from [itertools](https://docs.python.org/3/library/itertools.html)
- the `Fraction` class from [fractions](https://docs.python.org/3/library/fractions.html)
- the `Decimal` class from [decimal](https://docs.python.org/3/library/decimal.html)
- additional math functions defined in the [pymath](https://github.com/cjbassi/pymath/tree/master/pymath) folder

## Installation

```shell
pip install [--user] pymath2
```

**Note**: `~/.local/bin` should be in your `$PATH` for `--user` installs.

## Usage

Run an expression from the command line:

```shell
> pymath 'factorial(5)+1'
121
```

Or perform multiple calculations in the Python repl:

```shell
> pymath
>>> xgcd(5, 2)
(1, 1, -2)
>>> primes(5)
[2, 3, 5, 7, 11]
>>>
```

List all available functions:

```shell
pymath -l
```
