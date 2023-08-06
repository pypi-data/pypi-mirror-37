# ConfigEnv [![Build Status](https://travis-ci.org/Nydareld/ConfigEnv.svg?branch=master)](https://travis-ci.org/Nydareld/ConfigEnv) [![Coverage Status](https://coveralls.io/repos/github/Nydareld/ConfigEnv/badge.svg)](https://coveralls.io/github/Nydareld/ConfigEnv) [![PyPI version](https://badge.fury.io/py/ConfigEnv.svg)](https://badge.fury.io/py/ConfigEnv)![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ConfigEnv.svg)


Gestionnaire de configuration en json, ini avec overide possible en variable d’environnement

## install

with pip :

    pip install ConfigEnv

## how to use

You can actualy use ConfigEnv with either:
    - json file
    - ini file
    - environement variable

Notice than the environement variable will take over configuration files


### basic json exemple:
with the file :

```json
// config.json
{
    "AWS" : {
        "ACCESS_KEY_ID" : "toto"
    }
}
```

```python
from ConfigEnv import Config

config = Config("config.json")
print(config.get("AWS_ACCESS_KEY_ID"))
# prints toto
```

### overide file
you can add more file to veride configs
notice that the lib works with cache, so register all your config files before request config

```json
// config.json
{
    "AWS" : {
        "ACCESS_KEY_ID" : "toto"
    }
}
```

```ini
; config.ini
[AWS]
ACCESS_KEY_ID=tata
```

```python
from ConfigEnv import Config

config = Config("config.json")
config.addFile = Config("config.ini")
print(config.get("AWS_ACCESS_KEY_ID"))
# prints tata
```

### overide with environement variable

```json
// config.json
{
    "AWS" : {
        "ACCESS_KEY_ID" : "toto"
    }
}
```
with the environement variable : `AWS_ACCESS_KEY_ID=tata`
```python
from ConfigEnv import Config

config = Config("config.json")

print(config.get("AWS_ACCESS_KEY_ID"))
# prints tata
```

## devlopping guide

we advise you to fork the depot, and if you have goot feature, we would appreciate pull request

### install developement environement

with virtualenv :

    virtualenv -p python3 .venv
    source .venv/bin/activate

install depenencies :

    pip install -r requirements.txt

### test

run tests :

    python -m unittest tests

### coverage

run coverage

    coverage run --source=ConfigEnv -m unittest tests

report coverage

    coverage report -m

### release

create package :
    python3 setup.py sdist bdist_wheel

publish :
    python -m twine upload dist/*
