# Core classes and functions, reusable in any kind of Python application

**Features:**
* [exception classes to express common scenarios](https://github.com/RobertoPrevato/rocore/wiki/Common-exceptions)
* [implementation of models annotations, useful to implement validation of business objects](https://github.com/RobertoPrevato/rocore/wiki/Models-annotations)
* [friendly JSON encoder](https://github.com/RobertoPrevato/rocore/wiki/User-friendly-JSON-dumps), handling `datetime`, `date`, `time`, `UUID`, `bytes`
* [implementation of simple in-memory cache, supporting expiration of items and capped lists](https://github.com/RobertoPrevato/rocore/wiki/Caching)
* utilities to work with `folders` and paths
* [`StopWatch` implementation](https://github.com/RobertoPrevato/rocore/wiki/StopWatch-implementation)

## Installation

```bash
pip install rocore
```

## Documentation
Please refer to documentation in the project wiki: [https://github.com/RobertoPrevato/rocore/wiki](https://github.com/RobertoPrevato/rocore/wiki).

## Develop and run tests locally
```bash
pip install -r dev_requirements.txt

# run tests using automatic discovery:
pytest
```
