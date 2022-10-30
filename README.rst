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

|Binder|\ |PyPI version|\ |Anaconda|\ |CircleCI|\ |AppveyorCI|\ |Documentation Status|\ |codecov|\ |Zenodo|

tptp-lark-parser
================

``tptp-lark-parser`` is a parser for the `TPTP library
<https://tptp.org>`__ language using the `Lark parser
<https://github.com/lark-parser/lark>`__. For now, only CNF
sublanguage is supported.

How to Install
==============

The best way to install this package is to use ``pip``:

.. code:: sh

   pip install tptp-lark-parser

The package is also available on ``conda-forge``:
   
.. code:: sh

   conda install -c conda-forge tptp-lark-parser
   
One can also run it in a Docker container:

.. code:: sh

   docker build -t tptp-lark-parser https://github.com/inpefess/tptp-lark-parser.git
   docker run -it --rm -p 8888:8888 tptp-lark-parser jupyter-lab --ip=0.0.0.0 --port=8888

How to Use
==========

.. code:: python

   from tptp_lark_parser import TPTPParser

   tptp_parser = TPTPParser()
   parsed_text = tptp_parser.parse("cnf(test, axiom, ~ p(Y, X) | q(X, Y)).")
   clause_literals = parsed_text[0].literals
   
See `the
notebook <https://github.com/inpefess/tptp-lark-parser/blob/master/notebooks/usage-example.ipynb>`__
or run it in
`Binder <https://mybinder.org/v2/gh/inpefess/tptp-lark-parser/HEAD?labpath=usage-example.ipynb>`__
for more information.

More Documentation
==================

More documentation can be found
`here <https://tptp-lark-parser.readthedocs.io/en/latest>`__.

Similar Projects
================

There are many TPTP parsers in different languages:

* `C <https://github.com/TPTPWorld/SyntaxBNF>`__ (by TPTP's creator Geoff Sutcliffe)
* `Java <https://github.com/marklemay/tptpParser>`__
* `C++ <https://github.com/leoprover/tptp-parser>`__
* `JavaScript <https://www.npmjs.com/package/tptp>`__
* `Rust <https://github.com/MichaelRawson/tptp>`__
* `Common Lisp <https://github.com/lisphacker/cl-tptp-parser>`__
* `Scala <https://github.com/leoprover/scala-tptp-parser>`__
* `Haskell <https://github.com/aztek/tptp>`__
* `OCaml <https://github.com/Gbury/dolmen>`__

There also is `another parser in Python <https://github.com/AndrzejKucik/tptp_python_parser>`__ containing only the Lark syntax file.

How to Cite
===========

If you want to cite the `tptp-lark-parser` in your research paper,
please use the following doi:
`<https://doi.org/10.5281/zenodo.7040540>`__.

How to Contribute
=================

Please read `the Code of Conduct
<https://tptp-lark-parser.readthedocs.io/en/latest/code-of-conduct.html>`__
and then follow `the contribution guide
<https://tptp-lark-parser.readthedocs.io/en/latest/contributing.html>`__.

.. |PyPI version| image:: https://badge.fury.io/py/tptp-lark-parser.svg
   :target: https://badge.fury.io/py/tptp-lark-parser
.. |CircleCI| image:: https://circleci.com/gh/inpefess/tptp-lark-parser.svg?style=svg
   :target: https://circleci.com/gh/inpefess/tptp-lark-parser
.. |Documentation Status| image:: https://readthedocs.org/projects/tptp-lark-parser/badge/?version=latest
   :target: https://tptp-lark-parser.readthedocs.io/en/latest/?badge=latest
.. |codecov| image:: https://codecov.io/gh/inpefess/tptp-lark-parser/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/inpefess/tptp-lark-parser
.. |Binder| image:: https://mybinder.org/badge_logo.svg
   :target: https://mybinder.org/v2/gh/inpefess/tptp-lark-parser/HEAD?labpath=usage-example.ipynb
.. |AppveyorCI| image:: https://ci.appveyor.com/api/projects/status/7n0g3a3ag5hjtfi0?svg=true
   :target: https://ci.appveyor.com/project/inpefess/tptp-lark-parser
.. |Anaconda| image:: https://anaconda.org/conda-forge/tptp-lark-parser/badges/version.svg
   :target: https://anaconda.org/conda-forge/tptp-lark-parser
.. |Zenodo| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.7040540.svg
   :target: https://doi.org/10.5281/zenodo.7040540
