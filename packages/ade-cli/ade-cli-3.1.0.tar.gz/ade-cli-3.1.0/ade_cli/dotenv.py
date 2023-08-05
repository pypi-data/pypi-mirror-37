# -*- coding: utf-8 -*-
#
# Copyright 2016 - 2018  Ternaris.
# SPDX-License-Identifier: Apache-2.0

import os
import re
from collections import OrderedDict
from enum import Enum

from .utils import find_file


STATE = Enum('State', 'START KEY VALUE ESCAPE SINGLE DOUBLE DOUBLE_ESCAPE')


class InvalidCharacter(Exception):
    pass


class MissingValue(Exception):
    pass


class UnterminatedDoubleQuotes(Exception):
    pass


class UnterminatedSingleQuotes(Exception):
    pass


def load_dotenv(filename=None, envfile=None, cwd=None, env=None):
    assert bool(filename) ^ bool(envfile), "filename and envfile are mutually exclusive"
    filename = filename or '.env'
    envfile = envfile or find_file(filename=filename, cwd=cwd)
    envvars = read_vars(envfile.read_text()) if envfile else {}
    env = os.environ if env is None else env
    for k, v in envvars.items():
        if k not in env:
            env[k] = v
    return envfile


def read_vars(string):
    # pylint: disable=too-many-branches,too-many-statements
    env = OrderedDict()
    idx = 0
    state = STATE.START
    key = value = None
    while idx < len(string):
        char = string[idx]

        if state == STATE.START:
            if char == '#':
                try:
                    idx = string.index('\n', idx + 1)
                except ValueError:
                    idx = len(string)
                    continue

            elif char.isspace():
                pass

            elif char == 'e' and string[idx:idx + 7] == 'export ':
                idx += 6

            elif char.isalpha() and char.isupper():
                assert key is None, key
                state = STATE.KEY
                key = char

            else:
                raise InvalidCharacter(char, idx)

        elif state == STATE.KEY:
            if re.match(r'[0-9A-Z_]', char):
                key += char

            elif char == '=':
                assert value is None, value
                state = STATE.VALUE
                value = ''

            elif char.isspace():
                raise MissingValue(key)

            else:
                raise InvalidCharacter(char, idx)

        elif state == STATE.VALUE:
            if char == '\\':
                state = STATE.ESCAPE

            elif char == "'":
                state = STATE.SINGLE

            elif char == '"':
                state = STATE.DOUBLE

            elif char in '$`':
                raise InvalidCharacter(char, idx)

            elif char.isspace():
                assert key is not None
                assert value is not None
                env[key] = value
                key = value = None
                state = STATE.START

            else:
                value += char

        elif state == STATE.ESCAPE:
            if char == '\n':
                pass

            else:
                value += char

            state = STATE.VALUE

        elif state == STATE.SINGLE:
            if char == "'":
                state = STATE.VALUE

            else:
                value += char

        elif state == STATE.DOUBLE:
            if char == '\\':
                state = STATE.DOUBLE_ESCAPE

            elif char == '"':
                state = STATE.VALUE

            elif char in '$`':
                raise InvalidCharacter(char, idx)

            else:
                value += char

        elif state == STATE.DOUBLE_ESCAPE:  # pragma: no branch
            if char == '\n':
                pass

            elif char in '$`"\\':
                value += char

            else:
                value += '\\' + char

            state = STATE.DOUBLE

        assert state in STATE, state
        idx += 1

    if state == STATE.VALUE:
        assert key is not None
        assert value is not None
        env[key] = value
        key = value = None
        state = STATE.START

    elif state == STATE.DOUBLE:
        raise UnterminatedDoubleQuotes(key)

    elif state == STATE.SINGLE:
        raise UnterminatedSingleQuotes(key)

    assert value is None, value

    if key is not None:
        raise MissingValue(key)

    assert state == state.START, (state, key, value)

    return env
