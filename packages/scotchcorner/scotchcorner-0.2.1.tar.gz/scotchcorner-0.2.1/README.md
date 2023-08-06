# scotchcorner

[![GitHub version](https://badge.fury.io/gh/mattpitkin%2Fscotchcorner.svg)](https://badge.fury.io/gh/mattpitkin%2Fscotchcorner)
[![Build Status](https://travis-ci.org/mattpitkin/scotchcorner.svg?branch=master)](https://travis-ci.org/mattpitkin/scotchcorner)
[![PyPI version](https://badge.fury.io/py/scotchcorner.svg)](https://badge.fury.io/py/scotchcorner)

Greatly inspired by [corner.py](https://github.com/dfm/corner.py), this is an attempt to create a 
slightly different "corner" plot (and possibly the only one named after a [major junction on
the A1](https://en.wikipedia.org/wiki/Scotch_Corner)) for showing different combinations of projections of samples from
a multi-dimensional parameter space.

## Installation

This code requires numpy, scipy and [matplotlib](http://matplotlib.org), with a matplotlib version greater than or equal to 2.0.

The repository can be cloned and then installed using:

``python setup.py install``

or for (Linux) system-wide installation use:

``sudo python setup.py install``

or, using pip with:

``pip install scotchcorner``

## Example

Here's an example of the kind of plot you could produce:

![Example plot](example.png)

## Documentation

Documentation of the code can be found [here](http://scotchcorner.readthedocs.org/en/latest/).

If you have any suggestions/contributions for the code please create an issue, or fork and generate a pull request.

[![DOI](https://zenodo.org/badge/48458682.svg)](https://zenodo.org/badge/latestdoi/48458682)

Copyright &copy; 2016 Matthew Pitkin

Release under the MIT License
