# -*- coding: utf-8 -*-
#
# Copyright 2017 - 2018  Ternaris.
# SPDX-License-Identifier: Apache-2.0

"""Utility functions"""

import asyncio
import os
import sys
from contextlib import contextmanager
from functools import update_wrapper
from pathlib import Path
from shlex import quote
from subprocess import PIPE, run as _run

import click

ECHO = bool(os.environ.get('ECHO'))


def click_asyncio_loop(func):
    """Pass asyncio loop into function, being close upon ctx.close."""
    def new_func(*args, **kw):
        loop = asyncio.get_event_loop()
        ctx = click.get_current_context()
        ctx.call_on_close(loop.close)
        return func(loop, *args, **kw)
    return update_wrapper(new_func, func)


def find_file(filename, cwd=None, parent=False):
    """Find file starting from cwd upwards.

    Return parent instead of file if parent is set to True.
    """
    path = Path(cwd or '.').absolute()
    while True:
        envfile = path / filename
        if envfile.exists():
            return envfile.parent if parent else envfile
        if path == path.parent:
            return None
        path = path.parent


def get_timezone():
    """Determine timezone on host system."""
    try:
        return Path('/etc/timezone').read_text().strip()
    except FileNotFoundError:
        return '/'.join(Path('/etc/localtime').resolve().parts[-2:])


@contextmanager
def launch_pdb_on_exception(launch=True):
    """Return contextmanager launching pdb upon exception.

    Use like this, to toggle via env variable:

    with launch_pdb_on_exception(os.environ.get('PDB')):
        cli()
    """
    # pylint: disable=bare-except,no-member
    try:
        yield
    except:  # noqa
        if launch:
            import pdb
            pdb.xpm()
        else:
            raise


def run(cmdargs, *args, check=True, **kw):
    """Wrap subprocess.run optionally echoing commands."""
    if ECHO:
        if kw.get('shell'):
            print(cmdargs)
        else:
            print(' '.join([quote(x) for x in cmdargs]), file=sys.stderr)

    cwd = kw.pop('cwd', None)
    if isinstance(cwd, Path):
        cwd = bytes(cwd)
    kw['cwd'] = cwd

    if check == 'exit':
        cp = _run(cmdargs, *args, check=False, **kw)
        if cp.returncode != 0:
            sys.exit(cp.returncode)
    else:
        cp = _run(cmdargs, *args, check=check, **kw)

    return cp


def runout(*args, **kw):
    """Run cmd and return its stdout."""
    return run(*args, **kw, stdout=PIPE).stdout.decode('utf-8')


def shell(cmd, *args, check=True, **kw):
    """Run cmd through shell."""
    return run(cmd, *args, shell=True, check=check, **kw)


def shellout(*args, **kw):
    """Run cmd through shell and return its stdout."""
    return shell(*args, **kw, stdout=PIPE).stdout.decode('utf-8')


def splitjoin(help_str):
    """Split into lines, strip and rejoin with spaces.

    This allows formatting multi-line help strings for click options
    nicely, while not introducing linebreaks, e.g.

    @click.option('--foo', help=splitjoin('''
        First line.
        Seconds line.
        All actually being one line.
    '''
    """
    return ' '.join(x.strip() for x in help_str.splitlines())
