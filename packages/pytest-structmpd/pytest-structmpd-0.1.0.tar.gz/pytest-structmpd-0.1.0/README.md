# pytest-structmpd

[pytest](https://docs.pytest.org/en/latest/) plugin, provide structured temporary directories, easier to invest errors and failures.

## Overview

`tmpdir`, standard fixture in pytest, crates temporary directories like:

```
/tmp/pytest-of-<username>/
├── pytest-0
├── pytest-1
│   └── <test_function_name>
├── pytest-2
│   └── <test_function_name>
```

`structmpd` is like `tmpdir` but structured, followed session name and function name, like:

```
/tmp/pytest-session-<random>/
├── <test_function_name>
├── <test_function_name>
├── <test_class_name>
│   └── <test_method_name>
```

Temporary directories created by `structmpd` is removed after testing. This remove process can be controlled by option, see following sections.

## Support

- Python 2.7.15+ / 3.5+ / 3.6+

## Install

**Required**

- pytest 3.5+

```bash
$ pip install pytest-structmpd
```

from source

```bash
$ git clone https://github.com/disktnk/pytest-structmpd
$ cd pytest-structmpd
$ pip install -e .
```

## Usage

### 1. Setup

Add `structmpd` plugin in a target tests module

*conftest.py*

```python
pytest_plugins = ['structmpd']
```

or run pytest with `-p structmpd`

```bash
$ pytest -p structmpd
```

more detail, see [Installing and Using plugins](https://docs.pytest.org/en/latest/plugins.html)

### 2. Use as fixture

`tmpfuncdir` and `tmpsessiondir` are provided as fixture, use them on target functions.

- `tmpfuncdir`: a temporary directory for the target test function
- `tmpsessiondir`: a root directory of all temporary directories

Examples:

```python
def test_something(tmpfuncdir):
    # 'tmpfuncdir' is for this 'test_something' function


@pytest.mark.parametrize('param', [-1, 0, 1])
def test_something_with_param(param, tmpfuncdir):
    # 'tmpfuncdir' supports parameterized test, not conflicts with others


class TestCustomClass(object):

    def test_cls_method(self, tmpfuncdir):
        # 'tmpfuncdir' supports methods, the temporary directory is placed
        # under 'TestCustomClass' directory.
```

## Option

```bash
$ pytest \
--structmpd-root /path/to/tmp \
--structmpd-name original_name \
--structmpd-leave
```

* `--structmpd-root`: Directory path. On default a directory provided by OS is used, more detail, see [tempfile](https://docs.python.org/3.6/library/tempfile.html)
* `--structmpd-name`: Top directory name. On default session name like `pytest-module0` is used.
* `--structmpd-leave`: Not remove temporary directories created by this plugin if set.
