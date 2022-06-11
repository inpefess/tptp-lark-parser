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

# noqa D205
"""
CNF Parser.
===========
"""
import dataclasses
import json
from typing import Dict, Optional, Tuple, Union

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
    Variable,
)


def _load_token_lists(
    tokens_filename: str,
) -> Tuple[Dict[str, int], Dict[str, int], Dict[str, int]]:
    with open(tokens_filename, "r", encoding="utf-8") as tokens_file:
        tokens = json.load(tokens_file)
    return (
        {v: k for k, v in enumerate(tokens["variables"])},
        {v: k for k, v in enumerate(tokens["functions"])},
        {v: k for k, v in enumerate(tokens["predicates"])},
    )


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
    ...    cnf(this_is_a_test_case, axiom, f4(X1,f1(X2),f3(X3,f2)) = f4(X1,X2,f5)
    ...    | ~ p2(f4(X1),f1(X2)) | $false | p3,
    ...    inference(resolution, [], [this, that, third])).
    ... ''')
    >>> cnf_parser = CNFParser()
    >>> cnf_parser.function_map
    {'$not#a&function^': 0}
    >>> cnf_parser.predicate_map
    {'$false': 0, '=': 1, '!=': 2}
    >>> cnf_parser.variable_map
    {'X': 0}
    >>> cnf_parser.transform(lark_parsed_tree)
    Traceback (most recent call last):
    ...
    lark.exceptions.VisitError: Error trying to process rule "variable":
    <BLANKLINE>
    unknown symbol: X1
    >>> cnf_parser.extendable = True
    >>> cnf_parser.transform(lark_parsed_tree)
    cnf(this_is_a_test_case, axiom, f4(X1,f1(X2),f3(X3,f2)) = f4(X1,X2,f5) | ~p3(f4(X1),f1(X2)) | $false() | p4(), inference(resolution, [], [this, that, third])).
    >>> cnf_parser.function_map
    {'$not#a&function^': 0, 'f1': 1, 'f2': 2, 'f3': 3, 'f4': 4, 'f5': 5}
    >>> cnf_parser.predicate_map
    {'$false': 0, '=': 1, '!=': 2, 'p2': 3, 'p3': 4}
    """

    def __init__(
        self, tokens_filename: Optional[str] = None, extendable: bool = False
    ):
        """
        Initialize functional and predicate symbols lists.

        :param tokens_filename: a filename of known tokens storage
        :param extendable: when set to ``False``, the parser fails
            when encounters new symbols
        """
        super().__init__()
        if tokens_filename is None:
            self.function_map: Dict[str, int] = {"$not#a&function^": 0}
            self.predicate_map: Dict[str, int] = {
                FALSEHOOD_SYMBOL: FALSEHOOD_SYMBOL_ID,
                EQUALITY_SYMBOL: EQUALITY_SYMBOL_ID,
                INEQUALITY_SYMBOL: INEQUALITY_SYMBOL_ID,
            }
            self.variable_map: Dict[str, int] = {"X": 0}
        else:
            (
                self.variable_map,
                self.function_map,
                self.predicate_map,
            ) = _load_token_lists(tokens_filename)
        self.extendable = extendable

    def __default_token__(self, token):
        """All the tokens we return as is."""
        return token.value

    def __default__(self, data, children, meta):
        """Pop one element lists.

        By default, if we see a list of only one element, we return that
        element, not the whole list.
        """
        if len(children) == 1:
            return children[0]
        return children

    def _function(self, children):
        """Functional symbol with arguments."""
        function_name = children[0]
        function_id = self._get_symbol_id(function_name, Function)
        if len(children) > 1:
            return Function(function_id, tuple(children[1]))
        return Function(function_id, ())

    def _get_symbol_id(
        self, symbol: str, symbol_type: Union[Variable, Function, Predicate]
    ) -> int:
        """
        Get an integer ID for a symbol.

        :param symbol: a predicate or functional symbol, or a variable name
        :returns: an integer ID
        """
        if symbol_type == Variable:
            symbol_map = self.variable_map
        else:
            symbol_map = (
                self.function_map
                if symbol_type == Function
                else self.predicate_map
            )
        if symbol not in symbol_map:
            if self.extendable:
                symbol_map.update({symbol: 1 + max(symbol_map.values())})
            else:
                raise ValueError(f"unknown symbol: {symbol}")
        return symbol_map[symbol]

    def fof_defined_plain_formula(self, children):
        """
        Predicate with or without arguments.

        <fof_defined_plain_formula> :== <defined_proposition> | <defined_predicate>(<fof_arguments>)
        """
        return self._predicate(children)

    def fof_plain_term(self, children):
        """
        Functional symbol with or without (a constant) arguments.

        <fof_plain_term>       ::= <constant> | <functor>(<fof_arguments>)
        """
        return self._function(children)

    def fof_defined_term(self, children):
        """
        Another way to describe a functional symbol.

        <fof_defined_term>     ::= <defined_term> | <fof_defined_atomic_term>
        """
        return self._function(children)

    def variable(self, children):
        """
        Variable (supposed to be universally quantified).

        <variable>             ::= <upper_word>
        """
        return Variable(self._get_symbol_id(children[0], Variable))

    @staticmethod
    def fof_arguments(children):
        """
        List of arguments, organised in pairs.

        <fof_arguments>        ::= <fof_term> | <fof_term>,<fof_arguments>
        """
        result = ()
        for item in children:
            if not isinstance(item, (Variable, Function)):
                result = result + tuple(item)
            else:
                result = result + (item,)
        return result

    @staticmethod
    def literal(children):
        """
        Literal is a possible negated predicate.

        <literal>              ::= <fof_atomic_formula> | ~ <fof_atomic_formula> | <fof_infix_unary>
        """
        if children[0] == "~":
            return Literal(True, children[1])
        if isinstance(children[0], Predicate):
            if children[0].name == INEQUALITY_SYMBOL_ID:
                return Literal(
                    negated=True,
                    atom=Predicate(
                        name=EQUALITY_SYMBOL_ID,
                        arguments=children[0].arguments,
                    ),
                )
        return Literal(False, children[0])

    def _predicate(self, children):
        """Predicates are atomic formulae."""
        predicate_id = self._get_symbol_id(children[0], Predicate)
        if len(children) > 1:
            return Predicate(predicate_id, tuple(children[1]))
        return Predicate(predicate_id, ())

    def fof_plain_atomic_formula(self, children):
        """
        Another way for writing predicates.

        <fof_plain_atomic_formula> :== <proposition> | <predicate>(<fof_arguments>)
        """
        return self._predicate(children)

    def fof_defined_infix_formula(self, children):
        """
        Translte predicates in the infix form to the prefix.

        <fof_defined_infix_formula> ::= <fof_term> <defined_infix_pred> <fof_term>
        """
        predicate_id = self._get_symbol_id(children[1], Predicate)
        return Predicate(predicate_id, (children[0], children[2]))

    def fof_infix_unary(self, children):
        """
        Translate predicates in the infix form to the prefix.

        <fof_infix_unary>      ::= <fof_term> <infix_inequality> <fof_term>
        """
        predicate_id = self._get_symbol_id(children[1], Predicate)
        return Predicate(predicate_id, (children[0], children[2]))

    @staticmethod
    def disjunction(children):
        """
        Clause structure.

        <disjunction>          ::= <literal> | <disjunction> <vline> <literal>
        """
        if len(children) == 1:
            if (
                children[0].atom.name == FALSEHOOD_SYMBOL_ID
                and not children[0].negated
            ):
                return Clause(tuple())
            return Clause(tuple(children))
        literals = ()
        for item in (children[0], children[2]):
            if isinstance(item, Clause):
                literals = literals + item.literals
            else:
                literals = literals + (item,)
        return Clause(literals)

    @staticmethod
    def cnf_annotated(children):
        """
        Annotated CNF formula (clause).

        <cnf_annotated>        ::= cnf(<name>,<formula_role>,<cnf_formula> <annotations>).
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
    def inference_record(children):
        """
        Inference record (parents and rule).

        <inference_record>     :== inference(<inference_rule>,<useful_info>,
        <inference_parents>)
        """
        return {"inference_record": (children[0], tuple(children[2]))}

    @staticmethod
    def annotations(children):
        """
        Annotation (we care only about inference info from it).

        <annotations>          ::= ,<source><optional_info> | <null>
        """
        if isinstance(children, list):
            if len(children) == 1:
                return tuple(children[0])
        return children

    @staticmethod
    def parent_info(children):
        """
        Inference parents.

        <parent_info>          :== <source><parent_details>
        """
        return children[0]

    @staticmethod
    def parent_list(children):
        """
        Inference parents lits.

        <parent_list>          :== <parent_info> | <parent_info>,<parent_list>
        """
        if len(children) == 2:
            return (children[0],) + tuple(children[1])
        return children
