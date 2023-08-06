# pyver

## What is this?

This script simplifies the management of a Python project's versionning.
With a simple command, you can update at the same time your package's version, that written
in `setup.py`, and create a git tag for it.


## How do I use it?

You can install it from [pypi](https://pypi.org/project/python-versionning/): just run
`pip install python_versionning` (there's another project called pyver).

Now, provided the structure of your project respects the commonly used, you can run:

```bash
$ python3 -m pyver
1.0.0

$ python3 -m pyver bump minor
Version will be bumped from 1.0.0 to 1.1.0. Are you sure? [yes]/[no]
> y
Bumped version to 1.1.0
```

This will wrote `version="1.1.0"` in the `setup.py` file, `__version__ = "1.1.0"` in the
`__init__.py` file, and create a `1.1.0` git tag.
