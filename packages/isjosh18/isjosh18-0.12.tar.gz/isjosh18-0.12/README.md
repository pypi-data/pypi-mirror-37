# Is Josh 18?

[![Build Status](https://travis-ci.org/numirias/python-isjosh18.svg?branch=master)](https://travis-ci.org/numirias/python-isjosh18)
[![codecov](https://codecov.io/gh/numirias/python-isjosh18/branch/master/graph/badge.svg)](https://codecov.io/gh/numirias/python-isjosh18)
[![Python Versions](https://img.shields.io/pypi/pyversions/isjosh18.svg)](https://pypi.python.org/pypi/isjosh18)

A command-line interface to determine if Josh has turned 18 yet.


It's using the API provided by [https://hasjoshturned18yet.com/](https://hasjoshturned18yet.com/).

![Example](https://i.imgur.com/sCzdEW7.gif)


## Installation

    $ pip install isjosh18 --upgrade


## Usage

    $ isjosh18 -h
    usage: isjosh80 [-h] [--balloons] [-f] [--frequency FREQUENCY]
                    [--speed SPEED] [--width WIDTH] [--duration DURATION]

    Is Josh 18?

    optional arguments:
      -h, --help            show this help message and exit
      --balloons            Add balloons
      -f, --force           Force Josh to be 18
      --frequency FREQUENCY
                            Balloon frequency
      --speed SPEED         Balloon speed
      --width WIDTH         Screen width
      --duration DURATION   How many seconds the party should last (0: party on
                            forever)
