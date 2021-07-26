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

 |Binder|\ |PyPI version|\ |CircleCI|\ |Documentation Status|\ |codecov|

tptp-lark-parser
================

``tptp-lark-parser`` is an `OpenAI Gym <https://gym.openai.com/>`__
environment for reinforcement learning (RL) agents capable of proving
theorems. Currently, only theorems written in `TPTP
library <http://tptp.org>`__ formal language in clausal normal form
(CNF) are supported. ``tptp-lark-parser`` implements the ‘given clause’
algorithm (similar to one used in
`Vampire <https://github.com/vprover/vampire>`__ and `E
Prover <https://github.com/eprover/eprover>`__). Being written in
Python, ``tptp-lark-parser`` was inspired by
`PyRes <https://github.com/eprover/PyRes>`__. In contrast to monolithic
architecture of a typical Automated Theorem Prover (ATP),
``tptp-lark-parser`` gives different agents opportunities to select
clauses themselves and train from their experience. Combined with a
particular agent, ``tptp-lark-parser`` can work as an ATP.

``tptp-lark-parser`` can be interesting for RL practitioners willing to
apply their experience to theorem proving without coding all the
logic-related stuff themselves. It also can be useful for automated
deduction researchers who want to create an RL-empowered ATP.

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
