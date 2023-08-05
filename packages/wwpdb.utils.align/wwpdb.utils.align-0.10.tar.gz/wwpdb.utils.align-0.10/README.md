
## Pairwise Sequence Alignment Tools

A collection of sequence alignment tools

### Installation

Download the library source software from the project repository:

```bash

git clone --recurse-submodules https://github.com/wwpdb/py-wwpdb_utils_align.git

```

Optionally, run test suite (Python versions 2.7, 3.6, and 3.7) using
[setuptools](https://setuptools.readthedocs.io/en/latest/) or
[tox](http://tox.readthedocs.io/en/latest/example/platform.html):

```bash
python setup.py test

or simply run

tox
```

Installation is via the program [pip](https://pypi.python.org/pypi/pip).  To run tests
from the source tree, the package must be installed in editable mode (i.e. -e):

```bash
pip install -e .

or

pip install wwpdb.utils.align

```