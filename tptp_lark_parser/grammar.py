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
Grammar
********
"""
from dataclasses import dataclass, field
from typing import Optional, Tuple, Union
from uuid import uuid1

FALSEHOOD_SYMBOL = "$false"
FALSEHOOD_SYMBOL_ID = 0
EQUALITY_SYMBOL = "="
EQUALITY_SYMBOL_ID = 1
INEQUALITY_SYMBOL = "!="
INEQUALITY_SYMBOL_ID = 2


@dataclass(frozen=True)
class Variable:
    """
    A variable is characterised only by its name.

    .. _variable:
    """

    index: int


@dataclass(frozen=True)
class Function:
    """
    A functional symbol might be applied to a list of arguments.

    .. _Function:
    """

    index: int
    arguments: Tuple[Union[Variable, "Function"], ...]


Term = Union[Variable, Function]
Term.__doc__ = """
.. _Term:

Term is either a :ref:`Variable <Variable>` or a :ref:`Function <Function>`
"""


@dataclass(frozen=True)
class Predicate:
    """
    A predicate symbol might be applied to a list of arguments.

    .. _Predicate:
    """

    index: int
    arguments: Tuple[Term, ...]


Proposition = Union[Predicate, Term]
Proposition.__doc__ = """
.. _Proposition:

Proposition is either a :ref:`Predicate <Predicate>` or a :ref:`Term <Term>`
"""


@dataclass(frozen=True)
class Literal:
    """
    Literal is an atom which can be negated or not.

    .. _Literal:
    """

    negated: bool
    atom: Predicate


@dataclass(frozen=True)
class Clause:
    """
    Clause is a disjunction of literals.

    .. _Clause:


    :param literals: a list of literals, forming the clause
    :param label: comes from the problem file or starts with ``inferred_`` if
         inferred during the episode
    :param role: formula role: axiom, hypothesis, ...
    :param inference_parents: a list of labels from which the clause was
         inferred. For clauses from the problem statement, this list is empty
    :param inference_rule: the rule according to which the clause was got from
         the ``inference_parents``
    :param processed: boolean value splitting clauses into unprocessed and
         processed ones; in the beginning, everything is not processed
    :param birth_step: a number of the step when the clause appeared in the
         unprocessed set; clauses from the problem have ``birth_step`` zero
    """

    literals: Tuple[Literal, ...]
    label: str = field(
        default_factory=lambda: "x" + str(uuid1()).replace("-", "_")
    )
    role: str = "lemma"
    inference_parents: Optional[Tuple[str, ...]] = None
    inference_rule: Optional[str] = None
    processed: Optional[bool] = None
    birth_step: Optional[int] = None
