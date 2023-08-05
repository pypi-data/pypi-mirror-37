# sausage-machine

[Python](https://www.python.org) tools for scheduling pipeline jobs.

Runs under Python 2.7, 3.5, 3.6, 3.7-dev, and [pypy](http://pypy.org/)
[Change log](CHANGELOG.md).
[![Build Status](https://travis-ci.org/VirologyCharite/sausage-machine.svg?branch=master)](https://travis-ci.org/VirologyCharite/sausage-machine)

## Installation

### From PyPI using pip

Using [pip](https://pypi.python.org/pypi/pip):

```sh
$ pip install sausage-machine
```

### From Git sources

Using [git](https://git-scm.com/downloads):

```sh
# Clone repository.
$ git clone https://github.com/VirologyCharite/sausage-machine
$ cd sausage-machine

# Install dependencies.
$ pip install -r requirements.txt

# Install.
$ python setup.py install
```

## Scripts

The `bin` directory of this repo contains the following Python scripts:

## Pipeline specification

A pipeline run is scheduled according to a specification file in JSON
format...
