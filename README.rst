..
  Copyright 2022 Boris Shminke

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

      https://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.

|Binder|\ |PyPI version|\ |CircleCI|\ |AppveyorCI|\ |Documentation Status|\ |codecov|

tptp-lark-parser
================

``tptp-lark-parser`` is an parser for the `TPTP library
<http://tptp.org>`__ language using the `Lark parser
<https://github.com/lark-parser/lark>`__.

How to Install
==============

The best way to install this package is to use ``pip``:

.. code:: sh

   pip install tptp-lark-parser
   
One can also run it in a Docker container:

.. code:: sh

   docker build -t tptp-lark-parser https://github.com/inpefess/tptp-lark-parser.git
   docker run -it --rm -p 8888:8888 tptp-lark-parser jupyter-lab --ip=0.0.0.0 --port=8888 --no-browser

How to use
==========

.. code:: python

   from tptp_lark_parser import TPTPParser

   tptp_parser = TPTPParser()
   parsed_text = tptp_parser.parse("cnf(test, axiom, ~ p(Y, X) | q(X, Y)).")
   clause_literals = parsed_text[0].literals
   
See `the
notebook <https://github.com/inpefess/tptp-lark-parser/blob/master/examples/example.ipynb>`__
or run it in
`Binder <https://mybinder.org/v2/gh/inpefess/tptp-lark-parser/HEAD?labpath=example.ipynb>`__
for more information.

How to Contribute
=================

`Pull requests <https://github.com/inpefess/tptp-lark-parser/pulls>`__ are
welcome. To start:

.. code:: sh

   git clone https://github.com/inpefess/tptp-lark-parser
   cd tptp-lark-parser
   # activate python virtual environment with Python 3.7+
   pip install -U pip
   pip install -U setuptools wheel poetry
   poetry install
   # recommended but not necessary
   pre-commit install

To check the code quality before creating a pull request, one might run
the script ``local-build.sh``. It locally does nearly the same as the CI
pipeline after the PR is created.

Reporting issues or problems with the software
==============================================

Questions and bug reports are welcome on `the
tracker <https://github.com/inpefess/tptp-lark-parser/issues>`__.

More documentation
==================

More documentation can be found
`here <https://tptp-lark-parser.readthedocs.io/en/latest>`__.

.. |PyPI version| image:: https://badge.fury.io/py/tptp-lark-parser.svg
   :target: https://badge.fury.io/py/tptp-lark-parser
.. |CircleCI| image:: https://circleci.com/gh/inpefess/tptp-lark-parser.svg?style=svg
   :target: https://circleci.com/gh/inpefess/tptp-lark-parser
.. |Documentation Status| image:: https://readthedocs.org/projects/tptp-lark-parser/badge/?version=latest
   :target: https://tptp-lark-parser.readthedocs.io/en/latest/?badge=latest
.. |codecov| image:: https://codecov.io/gh/inpefess/tptp-lark-parser/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/inpefess/tptp-lark-parser
.. |Binder| image:: https://mybinder.org/badge_logo.svg
   :target: https://mybinder.org/v2/gh/inpefess/tptp-lark-parser/HEAD?labpath=example.ipynb
.. |AppveyorCI| image:: https://ci.appveyor.com/api/projects/status/7n0g3a3ag5hjtfi0?svg=true
   :target: https://ci.appveyor.com/project/inpefess/tptp-lark-parser
