# -*- coding: utf-8 -*-
#
# Copyright 2017 - 2018  Ternaris.
# SPDX-License-Identifier: Apache-2.0

"""Command-line interface for ADE"""

import os
import sys
import time
from collections import defaultdict
from subprocess import DEVNULL

import click

from . import dotenv
from . import registry
from .config import load_config
from .docker import docker_exec, docker_run, docker_stop, update
from .docker import is_running, print_image_matrix
from .utils import click_asyncio_loop, launch_pdb_on_exception, run, splitjoin


ADERC = None
CFG = None


@click.group()
def ade():
    """Agile Development Environment."""


@ade.command('enter')
@click.option('-u', '--user', help='Enter ade as given user (e.g. root) instead of default')
@click.argument('cmd', required=False)
def ade_enter(cmd, user):
    """Enter environment, running optional command."""
    if not ADERC:
        print('ERROR: Needs to run from within project with .aderc file', file=sys.stderr)
        sys.exit(1)

    if not is_running(CFG.name):
        print('ERROR: ADE is not running, please start with: ade start', file=sys.stderr)
        sys.exit(1)

    docker_exec(CFG.name, cmd, user)


@ade.command('start')
@click.option('--check/--no-check', help='Check whether updates are available.')
@click.option('--enter/--no-enter', help='Enter environment after starting.')
@click.option('-f', '--force/--no-force', help='Force restart of running environment.')
@click.option('--select', multiple=True, help=splitjoin("""
    Select image tags to be used instead of configured defaults. Valid
    image tags are git tags and branches. To select one for a specific
    image use IMAGE:TAG (e.g. ade:ftr123) and only TAG to select
    it for all images for which it exists (e.g. release-42).
"""))
@click.argument('addargs', nargs=-1)
@click_asyncio_loop
def ade_start(loop, check, enter, force, addargs, select):
    """Start environment from within ADE project.

    ADDARGS are directly passed to docker run.
    """
    if not ADERC:
        print('ERROR: Needs to run from within project with .aderc file', file=sys.stderr)
        sys.exit(1)

    if not CFG.images:
        print('ERROR: No images defined, please set ADE_IMAGES', file=sys.stderr)
        sys.exit(1)

    if CFG.home == os.environ['HOME']:
        print('ERROR: ADE_HOME must be different from normal $HOME', file=sys.stderr)
        sys.exit(1)

    image_names = defaultdict(list)
    for img in CFG.images:
        image_names[img.name].append(img)
    for name, imgs in image_names.items():
        if len(imgs) > 1:
            msg = ''.join(['\n  {}'.format(img.fqn) for img in imgs])
            print('WARNING: Multiple images named {}:{}'.format(name, msg))
            sys.exit(1)

    selectors = []
    for sel in select:
        try:
            img_name, tag = sel.split(':')
        except ValueError:
            selectors.append((None, sel))
        else:
            selectors.insert(0, (img_name, tag))

    remote_images = []
    for img in CFG.images:
        if img.registry:
            remote_images.append(img)

    if selectors:
        try:
            loop.run_until_complete(registry.adjust_tags(remote_images, selectors))
        except registry.NoSuchImage as e:
            fqn = e.args[0].fqn  # pylint: disable=no-member
            print('ERROR: Image {} does not exist'.format(fqn), file=sys.stderr)
            sys.exit(1)
        except registry.NoSuchTag as e:
            print('ERROR: {} does not exists for {}; choose from:\n  {}'
                  .format(e.args[1], e.args[0], '  \n'.join(sorted(e.args[2]))), file=sys.stderr)
            sys.exit(1)

    tags = {x.tag for x in remote_images}
    unused_selectors = [x for x in selectors if x[1] not in tags]
    if unused_selectors:
        print('WARNING: Some select options did not match any images', file=sys.stderr)

    print('Starting {} with the following images:'.format(CFG.name))
    print_image_matrix(None, CFG.images)
    if check:
        loop.run_until_complete(update(CFG.name, remote_images))

    if is_running(CFG.name):
        if not force:
            print(
                '\nERROR: {} is already running. Use ade enter to enter or ade start -f to restart.\n'
                .format(CFG.name), file=sys.stderr
            )
            sys.exit(125)
        docker_stop(CFG.name)
        time.sleep(1)

    addargs += CFG.runargs
    run(['docker', 'rm', '-f', CFG.name], check=False, stdout=DEVNULL, stderr=DEVNULL)
    success = docker_run(name=CFG.name, image=CFG.images[0], home=CFG.home, addargs=addargs,
                         debug=CFG.debug, volume_images=CFG.images[1:])

    if not success:
        print('ERROR: Failed to start ade. Re-run with --debug to get more information.',
              file=sys.stderr)
        sys.exit(1)

    if enter:
        docker_exec(CFG.name)
    else:
        print('\nADE has been started, enter or run commands using: ade enter\n')


@ade.command('stop')
def ade_stop():
    """Stop ade environment."""
    if not ADERC:
        print('ERROR: Needs to run from within project with .aderc file', file=sys.stderr)
        sys.exit(1)

    docker_stop(CFG.name)


def cli():
    """Setuptools entrypoint"""
    global ADERC, CFG
    with launch_pdb_on_exception(os.environ.get('PDB')):
        ADERC = dotenv.load_dotenv('.aderc')
        CFG = load_config()
        from . import credentials
        credentials.CFG = CFG
        ade(auto_envvar_prefix='ADE')  # pylint: disable=unexpected-keyword-arg
