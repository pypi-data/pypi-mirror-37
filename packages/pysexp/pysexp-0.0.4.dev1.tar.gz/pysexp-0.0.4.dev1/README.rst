S-expression parser for Python
==============================

About
-----

`pysexp` is a simple S-expression parser/serializer.  It has
simple `load` and `dump` functions like `pickle`, `json` or `PyYAML`
module.

>>> from pysexp import loads, dumps
>>> loads('("a" "b")')
['a', 'b']
>>> print(dumps(['a', 'b']))
("a" "b")


You can install `pysexp` from PyPI_::

  pip install pysexp


Links
-----

* `Repository (at GitHub) <https://github.com/jd-boyd/pysexp>`_
* `Issue tracker (at GitHub) <https://github.com/jd-boyd/pysexp/issues>`_
* `PyPI <http://pypi.python.org/pypi/pysexp>`_
* `Travis CI <https://travis-ci.org/#!/jd-boyd/pysexp>`_

Origin
------

Originally forked from https://github.com/tkf/sexpdata


License
-------

`pysexp` is licensed under the terms of the BSD 2-Clause License.
See the source code for more information.
