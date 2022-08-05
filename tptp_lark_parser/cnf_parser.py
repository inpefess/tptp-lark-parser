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

# noqa D205, D400
"""
CNF Parser
===========
"""
import dataclasses
import json
from typing import Any, Dict, List, Optional, Tuple

from lark import Transformer

from tptp_lark_parser.grammar import (
    EQUALITY_SYMBOL,
    EQUALITY_SYMBOL_ID,
    FALSEHOOD_SYMBOL,
    FALSEHOOD_SYMBOL_ID,
    INEQUALITY_SYMBOL,
    INEQUALITY_SYMBOL_ID,
    Clause,
    Function,
    Literal,
    Predicate,
    Term,
    Variable,
)


def _load_token_lists(
    tokens_filename: str,
) -> Dict[str, Dict[str, int]]:
    with open(tokens_filename, "r", encoding="utf-8") as tokens_file:
        tokens = json.load(tokens_file)
    return {
        "variables": {v: k for k, v in enumerate(tokens["variables"])},
        "functions": {v: k for k, v in enumerate(tokens["functions"])},
        "predicates": {v: k for k, v in enumerate(tokens["predicates"])},
    }


class CNFParser(Transformer):
    """
    A parser for ``<cnf_formula>`` from Lark parser tree.

    Methods are not typed since nobody calls them directly.

    >>> import sys
    >>> import os
    >>> if sys.version_info.major == 3 and sys.version_info.minor >= 9:
    ...     from importlib.resources import files
    ... else:
    ...     from importlib_resources import files
    >>> from lark import Lark
    >>> lark_parser = Lark(
    ...     files("tptp_lark_parser")
    ...     .joinpath(os.path.join("resources", "TPTP.lark"))
    ...     .read_text(),
    ...     start="tptp_file"
    ... )
    >>> lark_parsed_tree = lark_parser.parse('''
    ...    cnf(test, axiom, f(X, g(Y), h(Z, c1)) = f(X, Y, c2)
    ...    | ~ better(f(X), g(Y)) | $false | this_is_a_test_case,
    ...    inference(resolution, [], [this, that, third])).
    ... ''')
    >>> cnf_parser = CNFParser()
    >>> cnf_parser.token_map["functions"]
    {'f': 0}
    >>> cnf_parser.transform(lark_parsed_tree)
    Traceback (most recent call last):
    ...
    lark.exceptions.VisitError: Error trying to process rule "fof_plain_term":
    <BLANKLINE>
    unknown symbol: g
    >>> cnf_parser.extendable = True
    >>> clause = cnf_parser.transform(lark_parsed_tree)
    >>> print(cnf_parser.pretty_print(clause))
    cnf(test, axiom, f(X,g(Y),h(Z,c1)) = f(X,Y,c2) | ~better(f(X), g(Y)) | $false() | this_is_a_test_case(), inference(resolution, [], [this, that, third])).
    >>> cnf_parser.token_map
    {'functions': {'f': 0, 'g': 1, 'c1': 2, 'h': 3, 'c2': 4, 'better': 5, 'this_is_a_test_case': 6}, 'predicates': {'$false': 0, '=': 1, '!=': 2, 'better': 3, 'this_is_a_test_case': 4}, 'variables': {'X0': 0, 'X1': 1, ..., 'X999': 999, 'X': 1000, 'Y': 1001, 'Z': 1002}}
    """

    def __init__(
        self, tokens_filename: Optional[str] = None, extendable: bool = False
    ):
        """
        Initialise functional and predicate symbols lists.

        :param tokens_filename: a filename of known tokens storage
        :param extendable: when set to ``False``, the parser fails
            when encounters new symbols
        """
        super().__init__()
        if tokens_filename is None:
            self.token_map = {
                "functions": {"f": 0},
                "predicates": {
                    FALSEHOOD_SYMBOL: FALSEHOOD_SYMBOL_ID,
                    EQUALITY_SYMBOL: EQUALITY_SYMBOL_ID,
                    INEQUALITY_SYMBOL: INEQUALITY_SYMBOL_ID,
                },
                "variables": {f"X{i}": i for i in range(1000)},
            }
        else:
            self.token_map = _load_token_lists(tokens_filename)
        self.token_lists: Dict[str, List[str]] = {
            key: list(value.keys()) for key, value in self.token_map.items()
        }
        self.extendable = extendable

    def __default_token__(self, token):
        """All the tokens we return as is."""
        return token.value

    def __default__(self, data, children: List[Any], meta):
        """Pop one element lists.

        By default, if we see a list of only one element, we return that
        element, not the whole list.
        """
        if len(children) == 1:
            return children[0]
        return children

    def _function(self, children: List[Any]):
        """Functional symbol with arguments."""
        function_name = children[0]
        function_id = self._get_symbol_id(function_name, "functions")
        if len(children) > 1:
            return Function(function_id, tuple(children[1]))
        return Function(function_id, ())

    def _get_symbol_id(self, symbol: str, symbol_type: str) -> int:
        """
        Get an integer ID for a symbol.

        :param symbol: a predicate or functional symbol, or a variable name
        :param symbol_type: a type of the symbol (variables, functions, or
            predicates)
        :returns: an integer ID
        :raises ValueError: if a symbol is not in a map and maps were defined
            as not extendable
        """
        symbol_map = self.token_map[symbol_type]
        symbol_list = self.token_lists[symbol_type]
        if symbol not in symbol_map:
            if self.extendable or symbol_type == "variables":
                symbol_map.update({symbol: 1 + max(symbol_map.values())})
                symbol_list.append(symbol)
            else:
                raise ValueError(f"unknown symbol: {symbol}")
        return symbol_map[symbol]

    def fof_defined_plain_formula(self, children: List[Any]):
        """
        Predicate with or without arguments.

        <fof_defined_plain_formula> :== <defined_proposition> | <defined_predicate>(<fof_arguments>)

        :param children: parsed tree node's children
        """
        return self._predicate(children)

    def fof_plain_term(self, children: List[Any]):
        """
        Functional symbol with or without (a constant) arguments.

        <fof_plain_term>       ::= <constant> | <functor>(<fof_arguments>)
        :param children: parsed tree node's children
        """
        return self._function(children)

    def fof_defined_term(self, children: List[Any]):
        """
        Another way to describe a functional symbol.

        <fof_defined_term>     ::= <defined_term> | <fof_defined_atomic_term>

        :param children: parsed tree node's children
        """
        return self._function(children)

    def variable(self, children: List[Any]):
        """
        Variable (supposed to be universally quantified).

        <variable>             ::= <upper_word>

        :param children: parsed tree node's children
        """
        return Variable(self._get_symbol_id(children[0], "variables"))

    @staticmethod
    def fof_arguments(children: List[Any]):
        """
        List of arguments, organised in pairs.

        <fof_arguments>        ::= <fof_term> | <fof_term>,<fof_arguments>

        :param children: parsed tree node's children
        """
        result: Tuple[Any, ...] = ()
        for item in children:
            if not isinstance(item, (Variable, Function)):
                result = result + tuple(item)
            else:
                result = result + (item,)
        return result

    @staticmethod
    def literal(children: List[Any]):
        """
        Literal is a possible negated predicate.

        <literal>              ::= <fof_atomic_formula> | ~ <fof_atomic_formula> | <fof_infix_unary>

        :param children: parsed tree node's children
        """
        if children[0] == "~":
            return Literal(True, children[1])
        if isinstance(children[0], Predicate):
            if children[0].index == INEQUALITY_SYMBOL_ID:
                return Literal(
                    negated=True,
                    atom=Predicate(
                        index=EQUALITY_SYMBOL_ID,
                        arguments=children[0].arguments,
                    ),
                )
        return Literal(False, children[0])

    def _predicate(self, children: List[Any]):
        """Predicates are atomic formulae."""
        predicate_id = self._get_symbol_id(children[0], "predicates")
        if len(children) > 1:
            return Predicate(predicate_id, tuple(children[1]))
        return Predicate(predicate_id, ())

    def fof_plain_atomic_formula(self, children: List[Any]):
        """
        Another way for writing predicates.

        <fof_plain_atomic_formula> :== <proposition> | <predicate>(<fof_arguments>)

        :param children: parsed tree node's children
        """
        return self._predicate(
            [
                self.token_lists["functions"][children[0].index],
                children[0].arguments,
            ]
        )

    def fof_defined_infix_formula(self, children: List[Any]):
        """
        Translate predicates in the infix form to the prefix.

        <fof_defined_infix_formula> ::= <fof_term> <defined_infix_pred> <fof_term>

        :param children: parsed tree node's children
        """
        predicate_id = self._get_symbol_id(children[1], "predicates")
        return Predicate(predicate_id, (children[0], children[2]))

    def fof_infix_unary(self, children: List[Any]):
        """
        Translate predicates in the infix form to the prefix.

        <fof_infix_unary>      ::= <fof_term> <infix_inequality> <fof_term>

        :param children: parsed tree node's children
        """
        predicate_id = self._get_symbol_id(children[1], "predicates")
        return Predicate(predicate_id, (children[0], children[2]))

    @staticmethod
    def disjunction(children: List[Any]):
        """
        Clause structure.

        <disjunction>          ::= <literal> | <disjunction> <vline> <literal>

        :param children: parsed tree node's children
        """
        if len(children) == 1:
            if (
                children[0].atom.index == FALSEHOOD_SYMBOL_ID
                and not children[0].negated
            ):
                return Clause(tuple())
            return Clause(tuple(children))
        literals: Tuple[Any, ...] = ()
        for item in (children[0], children[2]):
            if isinstance(item, Clause):
                literals = literals + item.literals
            else:
                literals = literals + (item,)
        return Clause(literals)

    @staticmethod
    def cnf_annotated(children: List[Any]):
        """
        Annotated CNF formula (clause).

        <cnf_annotated>        ::= cnf(<name>,<formula_role>,<cnf_formula> <annotations>).

        :param children: parsed tree node's children
        """
        clause = children[2]
        inference_rule = None
        inference_parents = None
        if isinstance(children[3], list):
            for annotation in children[3]:
                if isinstance(annotation, dict):
                    if "inference_record" in annotation:
                        inference_rule = annotation["inference_record"][0]
                        inference_parents = annotation["inference_record"][1]
        return dataclasses.replace(
            clause,
            label=children[0],
            role=children[1],
            inference_rule=inference_rule,
            inference_parents=inference_parents,
        )

    @staticmethod
    def inference_record(children: List[Any]):
        """
        Inference record (parents and rule).

        <inference_record>     :== inference(<inference_rule>,<useful_info>,
        <inference_parents>)

        :param children: parsed tree node's children
        """
        return {"inference_record": (children[0], tuple(children[2]))}

    @staticmethod
    def annotations(children: List[Any]):
        """
        Annotation (we care only about inference info from it).

        <annotations>          ::= ,<source><optional_info> | <null>

        :param children: parsed tree node's children
        """
        if isinstance(children, list):
            if len(children) == 1:
                return tuple(children[0])
        return children

    @staticmethod
    def parent_info(children: List[Any]):
        """
        Inference parents.

        <parent_info>          :== <source><parent_details>

        :param children: parsed tree node's children
        """
        return children[0]

    @staticmethod
    def parent_list(children: List[Any]):
        """
        Inference parents list.

        <parent_list>          :== <parent_info> | <parent_info>,<parent_list>

        :param children: parsed tree node's children
        """
        if len(children) == 2:
            return (children[0],) + tuple(children[1])
        return children

    def _term_to_tptp(self, term: Term) -> str:
        if isinstance(term, Function):
            function_name = self.token_lists["functions"][term.index]
            arguments = tuple(
                self._term_to_tptp(argument) for argument in term.arguments
            )
            if arguments != tuple():
                return f"{function_name}({','.join(arguments)})"
            return function_name
        return self.token_lists["variables"][term.index]

    def _literal_to_tptp(self, literal: Literal) -> str:
        negation = "~" if literal.negated else ""
        arguments = tuple(
            self._term_to_tptp(term) for term in literal.atom.arguments
        )
        if literal.atom.index == EQUALITY_SYMBOL_ID:
            return f"{negation}{arguments[0]} {EQUALITY_SYMBOL} {arguments[1]}"
        if literal.atom.index == FALSEHOOD_SYMBOL_ID:
            return f"{negation}{FALSEHOOD_SYMBOL}()"
        predicate_name = self.token_lists["predicates"][literal.atom.index]
        return f"{negation}{predicate_name}({', '.join(arguments)})"

    def pretty_print(self, clause: Clause) -> str:
        """
        Print a logical formula back to TPTP language.

        :param clause: a logical clause to print
        :returns: a TPTP string
        """
        res = f"cnf({clause.label}, {clause.role}, "
        for literal in clause.literals:
            res += self._literal_to_tptp(literal) + " | "
        if res[-2:] == "| ":
            res = res[:-3]
        if not clause.literals:
            res += FALSEHOOD_SYMBOL
        if (
            clause.inference_parents is not None
            and clause.inference_rule is not None
        ):
            res += (
                f", inference({clause.inference_rule}, [], ["
                + ", ".join(clause.inference_parents)
                + "])"
            )
        return res + ")."
