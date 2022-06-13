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
"""An example of parsing full TPTP CNF subset."""
import json
import logging
import os
import sys
from glob import glob
from typing import Optional

from tptp_lark_parser import TPTPParser


def _read_and_parse_file(
    tptp_parser: TPTPParser, problem_filename: str
) -> None:
    with open(problem_filename, "r", encoding="utf-8") as problem_file:
        problem_text = problem_file.read()
    tptp_parser.parse(problem_text)


def _get_logger(level: int) -> logging.Logger:
    logger = logging.getLogger()
    logger.setLevel(level)
    handler = logging.StreamHandler(sys.stdout)
    logger.addHandler(handler)
    return logger


def parse_tptp(
    tptp_folder: str,
    output_file: str,
    logging_level: int,
    tokens_filename: Optional[str],
    learn_new_tokens: bool,
) -> None:
    """
    Parse all TPTP CNF problems and write all symbols encountered.

    >>> if sys.version_info.major == 3 and sys.version_info.minor >= 9:
    ...     from importlib.resources import files
    ... else:
    ...     from importlib_resources import files
    >>> tptp_folder = (
    ...     files("tptp_lark_parser")
    ...     .joinpath(os.path.join("resources", "TPTP-mock"))
    ... )
    >>> temp_folder = getfixture("tmp_path")  # noqa: F821
    >>> output_file = os.path.join(temp_folder, "test.json")
    >>> os.path.exists(output_file)
    False
    >>> parse_tptp(tptp_folder, output_file, logging.FATAL, None, True)
    >>> parse_tptp(tptp_folder, output_file, logging.FATAL, output_file, False)

    :param tptp_folder: a folder with TPTP dump
    :param output_file: where to save tokens found
    :param logging_level: what to log
    :param tokens_filename: a filename of known tokens storage
    :param learn_new_tokens: if ``False``, then parsing fails when encounters
        an unknown token
    """
    logger = _get_logger(logging_level)
    tptp_parser = TPTPParser(tptp_folder, learn_new_tokens, tokens_filename)
    cnf_problems = sorted(
        [
            problem
            for problem in glob(
                os.path.join(tptp_folder, "Problems", "*", "*-*.p")
            )
            if "CSR" not in problem
            and "HWV" not in problem
            and "KRS" not in problem
            and "PLA" not in problem
            and "SWV" not in problem
            and "SYN" not in problem
            and "SYO" not in problem
        ]
    )
    for problem in cnf_problems:
        _read_and_parse_file(tptp_parser, problem)
        # we save lists on every iteration because the next one may fail
        tokens = {
            key: list(value.keys())
            for key, value in tptp_parser.cnf_parser.token_map.items()
        }
        with open(output_file, "w", encoding="utf-8") as tokens_file:
            json.dump(tokens, tokens_file)
        logger.info("%s done", problem)


if __name__ == "__main__":
    parse_tptp(
        os.path.join(os.environ["WORK"], "data", "TPTP-v8.0.0"),
        "tptp_tokens.json",
        logging.INFO,
        None,
        True,
    )  # pragma: no cover
