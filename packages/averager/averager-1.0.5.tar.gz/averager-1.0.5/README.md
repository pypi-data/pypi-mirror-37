# Getting started

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/3b275766803c4c188d03b924b6c22e19)](https://app.codacy.com/app/bensoyka/averager?utm_source=github.com&utm_medium=referral&utm_content=bsoyka/averager&utm_campaign=Badge_Grade_Dashboard)
[![Build Status](https://travis-ci.org/bsoyka/averager.svg?branch=master)](https://travis-ci.org/bsoyka/averager)
[![GitHub release](https://img.shields.io/github/release/bsoyka/averager.svg)](https://github.com/bsoyka/averager/releases)
[![PyPI](https://img.shields.io/pypi/v/averager.svg)](https://pypi.org/project/averager)
[![GitHub issues](https://img.shields.io/github/issues-raw/bsoyka/averager.svg)](https://github.com/bsoyka/averager/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr-raw/bsoyka/averager.svg)](https://github.com/bsoyka/averager/pulls)
[![License](https://img.shields.io/github/license/bsoyka/averager.svg)](https://github.com/bsoyka/averager/blob/master/LICENSE)

## Averager

This is the most basic class in the averager module.  It allows you to simply average any quantity of numbers.

```python
import averager
instance = averager.Averager
print(instance.average(1, 5))
# 3
```

### Usage

The Averager class allows you to make an instance, and then use its average method with any quantity of numbers as the parameters.  The average method will return a float object, or an int object if it is equivalent.  For example, instead of 3.0, it returns 3, but 5.5 stays the same.

```python
import averager
print(averager.Averager.average(1, 5))
# 3
```

## WeightedAverager

The WeightedAverager class is very similar to the Averager class, but the WeightedAverager class allows you to set different weights to be used when averaging numbers.

```python
import averager
instance = averager.WeightedAverager(a=1, b=2, c=3)
print(instance.average(a=1, c=2))
# 1.75
```

### Usage

Usage of the WeightedAverager class is similar to that of the Averager class.  First, initialize an instance of the class, passing keyword arguments with the labels for your numbers and the weights attached to those labels.  These labels will need to be used again.  Then, run the instance's average method, passing keyword arguments with some or all of the labels you specified in the initialization, as well as values for each one.  The method will take into account the weight for each number specified, and will average the numbers accordingly.

### Potential errors

* When initializing an instance of the WeightedAverager, if a weight below zero is passed, a ValueError will be raised.
* When running the average method, if a label is passed that does not have a weight assigned to it, a KeyError will be raised.

