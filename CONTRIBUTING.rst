.. highlight:: shell

Contributing
============

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/inpefess/tptp-lark-parser/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

``tptp-lark-parser`` could always use more documentation, whether as part of the
official ``tptp-lark-parser`` docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/inpefess/tptp-lark-parser/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `tptp-lark-parser` for local development.

1. Fork the `tptp-lark-parser` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/tptp-lark-parser.git

3. Install your local copy into a virtualenv. Assuming you have Python 3.6+ installed, this is how you set up your fork for local development::

    $ cd ./tptp-lark-parser/
    $ python -m venv ./venv
    $ source ./venv/bin/activate
    $ pip install -U pip wheel setuptools poetry
    $ poetry install

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass
   ``pydocstyle``, ``flake8``, ``pylint``, ``mypy`` and the tests::

    $ pydocstyle tptp-lark-parser
    $ flake8 tptp-lark-parser
    $ pylint tptp-lark-parser
    $ mypy tptp-lark-parser
    $ pytest
 
   If you are on Linux, you can also run a all-in-one script::

    $ ./local-build.sh 

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

When you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be
   updated. Put your new functionality into a function with a
   docstring. Add a new file to the ``doc`` folder if needed.
3. The pull request should work for Python 3.7, 3.8, 3.9, and 3.10.
   Check `the pull requests page
   <https://github.com/inpefess/tptp-lark-parser/pulls>`__ and make
   sure that the tests pass for all supported Python versions.

Tips
----

To run a subset of tests (all the tests in this repo are `doctests
<https://docs.python.org/3/library/doctest.html>`__)::

    $ py.test --doctest-modules tptp_lark_parser/cnf_parser.py

Deploying
---------

A reminder for the maintainers on how to deploy.
Make sure all your changes are committed (including an entry in HISTORY.rst).
Then run::

    $ tbump current-version
    $ tbump {a new version here}
    $ poetry publish --build

``poetry`` will then deploy to PyPI.

Code of Conduct
---------------
Please note that the ``tptp-lark-parser`` project is released with a Contributor Code of Conduct. By contributing to this project you agree to abide by its terms.
