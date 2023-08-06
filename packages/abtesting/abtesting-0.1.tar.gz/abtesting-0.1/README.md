# ABTesting
A simple Python package for evaluating A/B tests.

## Intro
The idea behind creating this package was to provide a __means for evaluating A/B tests__ which is free of dependencies such as ```scipy```. Despite that I've wanted to explore ways of developing my own Python package.

As I work a lot with A/B tests which involve conversion events, I thought a simple two sample __Z test__ for the equality of proportions would be a good starting point. Unfortunately, this is the __only__ testing method included in this package so far. However, I will continue to add more A/B test evaluation methods in the future.

## Installation
The package installation can easily be done from the command line with
```
$ pip install abtesting
```
The package doesn't depend on any but standard Python libraries such as ```math```.

## Files
The following files are inluded in this package:
- ```ABTest.py``` includes classes and functions for creating test groups and using special functions
- ```ZTest.py``` included classes and functions for performing Z test

## Usage
Import the package as usual with
```python
from abtesting import ABTest, ZTest
```
Let's come up with some fake data for our test and control groups. We need to parameters, the size of our group as well as the number of conversion events that were observed during the testing period. Both values can be used to estimate the sample mean / proporton.
```python
# Size
na = 351676
nb = 352899

# Proportions
pa = 1301 / na
pb = 1203 / nb
```
We can then instantiate both groups as TestGroup objects.
```python
group_a = ABTest.TestGroup(na, pa)
group_b = ABTest.TestGroup(nb, pb)
```
Finally, we compare the two sample means by using the test of our choice. In this case, we choose the Z test.
```python
ztest = ZTest(group_a, group_b, pooled=True)
ztest
```
```
Two sample Z test for equality of proportions (without continuity correction)

Summary:
-----------------------------------
Sample means A = 0.0037, B = 0.0034
Sample difference = 0.0003
95% confidence interval = (0.0000, 0.0006)
Z = 2.0489
p = 0.0202
df = 1
```

## Acknowledgements
Large parts of the core functionalities of this package would not have been there without sources like [Wikipedia](https://www.wikipedia.org) or [Stackoverflow](https://stackoverflow.com) and I've tried to include some of the sources within the code as possible.
