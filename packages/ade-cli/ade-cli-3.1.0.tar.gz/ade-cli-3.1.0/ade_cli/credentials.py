# -*- coding: utf-8 -*-
#
# Copyright 2018  Ternaris.
# SPDX-License-Identifier: Apache-2.0

import json
import os
import sys
from collections import OrderedDict

import click

from .utils import find_file


CFG = None
FILENAME = '.adecreds'


def create_credentials_file(filename):
    adehome = find_file('.adehome', parent=True)
    if adehome is None:
        print('ERROR: Not within an ade home!', file=sys.stderr)
        sys.exit(2)

    credsfile = adehome / filename
    try:
        f = open(credsfile, 'x+')
        os.chmod(credsfile, 0o600)
    except FileExistsError:
        f = open(credsfile, 'r+')
    f.close()
    return credsfile


def get_credentials(host):
    """Return username and token for host."""
    credsfile = find_file(FILENAME)
    if credsfile is None:
        credsfile = create_credentials_file(FILENAME)

    try:
        raw = credsfile.read_text()
        allcreds = json.loads(raw) if raw else {}
    except json.decoder.JSONDecodeError:
        print('ERROR: {} is not valid json!'.format(credsfile), file=sys.stderr)
        click.confirm('Do you want to wipe and recreate it', abort=True)
        allcreds = {}

    try:
        creds = allcreds.setdefault(host, {})
        username = creds['username']
        token = creds['token']
    except KeyError:
        print('Please provide credentials for', host)
        username = creds['username'] = click.prompt('Username', default=creds.get('username'))
        if host == CFG.registry:
            print("""
Create access token:

  https://{}/profile/personal_access_tokens

with scopes:

  read_registry
""".lstrip().format(CFG.gitlab))
        token = creds['token'] = click.prompt('Token', default=creds.get('token'))

    credsfile.write_text(json.dumps(allcreds, sort_keys=True, indent=2))

    return OrderedDict((
        ('username', username),
        ('token', token),
    ))
