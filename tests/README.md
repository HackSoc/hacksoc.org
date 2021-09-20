# Tests
Tests are written with Python's builtin [`unittest`][https://docs.python.org/3/library/unittest.html] library. If you can come up with more helpful tests, please do!

## Test methodology
Currently supported platforms include:
**Python** versions
 - 3.7
 - 3.8
 - 3.9

**Operating systems**:
 - Linux
 - Windows
 - MacOS

## Running tests
The test suite can be run with:
```
python -m unittest discover -s tests/
# with the venv activated

venv/bin/python -m unittest discover -s tests/
# otherwise
```