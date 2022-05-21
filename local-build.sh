#!/bin/bash

set -e
PACKAGE_NAME=tptp_lark_parser
cd doc
make clean html
cd ..
flake8 ${PACKAGE_NAME}
pylint ${PACKAGE_NAME}
mypy ${PACKAGE_NAME}
pytest
scc -i py ${PACKAGE_NAME}
