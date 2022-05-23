# Copyright 2022 Boris Shminke
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
TPTP Parser
===========
"""
import os
import sys
from typing import Tuple

from lark import Lark, Token

from tptp_lark_parser.cnf_parser import CNFParser
from tptp_lark_parser.grammar import Clause

if sys.version_info.major == 3 and sys.version_info.minor >= 9:
    # pylint: disable=no-name-in-module, import-error
    from importlib.resources import files  # type: ignore
else:  # pragma: no cover
    from importlib_resources import files  # pylint: disable=import-error


# pylint: disable=too-few-public-methods
class TPTPParser:
    """
    .. _tptp-parser:

    >>> from tptp_lark_parser.grammar import (Literal, Predicate, Variable,
    ...     Function)
    >>> tptp_parser = TPTPParser()
    >>> clause = Clause(literals=(Literal(True, Predicate("=", (Function("this_is_a_test_case", (Variable("X"), )), Variable("Y")))), Literal(False, Predicate("=", (Function("f", ()), Function("g", ())))), Literal(False, Predicate("p", (Variable("X"),)))), inference_rule="resolution", inference_parents=("one", "two"))
    >>> tptp_parser.parse(str(clause))[0] == clause
    True
    >>> print(clause.to_java())
    boolean x...(Object X, Object Y) {
        return !(this_is_a_test_case(X) == Y) || (f() == g()) || p(X);
    }
    >>> print(clause.to_python())
    def x...(X, Y):
        return ~(this_is_a_test_case(X) == Y) | (f() == g()) | p(X)

    >>> empty_clause = Clause(literals=())
    >>> tptp_parser.parse(str(empty_clause))[0] == empty_clause
    True
    >>> print(empty_clause.to_java())
    boolean x...() {
        return false;
    }
    >>> print(empty_clause.to_python())
    def x...():
        return false

    >>> tptp_text = (
    ...     files("tptp_lark_parser")
    ...     .joinpath(os.path.join(
    ...         "resources", "TPTP-mock", "Problems", "TST", "TST001-1.p"
    ...     ))
    ...     .read_text()
    ... )
    >>> parsed_clauses = tptp_parser.parse(
    ...     tptp_text,
    ...     files("tptp_lark_parser")
    ...     .joinpath(os.path.join("resources", "TPTP-mock"))
    ... )
    >>> print("\\n".join(map(str, parsed_clauses)))
    cnf(this_is_a_test_case_1, hypothesis, this_is_a_test_case(test_constant), inference(resolution, [], [one, two])).
    cnf(this_is_a_test_case_2, hypothesis, ~this_is_a_test_case(test_constant)).
    cnf(test_axiom, axiom, test_constant = test_constant_2).
    cnf(test_axiom_2, axiom, ~test_constant = 0).
    """

    def __init__(self):
        # pylint: disable=unspecified-encoding
        self.parser = Lark(
            files("tptp_lark_parser")
            .joinpath(os.path.join("resources", "TPTP.lark"))
            .read_text(),
            start="tptp_file",
        )

    def parse(
        self, tptp_text: str, tptp_folder: str = "."
    ) -> Tuple[Clause, ...]:
        """
        recursively parse a string containing a TPTP problem

        :param tptp_text: a name of a problem (or axioms) file
        :param tptp_folder: a folder containing TPTP database
        :returns: a list of clauses (including those of the axioms)
        """
        problem_tree = self.parser.parse(tptp_text)
        clauses = tuple(
            CNFParser().transform(cnf_formula)
            for cnf_formula in problem_tree.find_data("cnf_annotated")
        )
        for include in problem_tree.find_data("include"):
            token = include.children[0]
            if isinstance(token, Token):
                with open(
                    os.path.join(tptp_folder, token.value.replace("'", "")),
                    "r",
                    encoding="utf-8",
                ) as included_file:
                    clauses = clauses + self.parse(
                        included_file.read(), tptp_folder
                    )
        return clauses
