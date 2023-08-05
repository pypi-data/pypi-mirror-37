# -*- coding: utf-8 -*-
#
# Copyright 2017 - 2018  Ternaris.
# SPDX-License-Identifier: Apache-2.0

import json
import os
import sys
from subprocess import CalledProcessError, DEVNULL, PIPE, Popen

from ade_cli import __version__ as VERSION
from .registry import Image, login, update_image
from .utils import get_timezone
from .utils import run, runout, shell, shellout


def docker_exec(name, cmd=None, user=None):
    """Enter container or run command inside container."""
    if not user:
        user = shellout('id -un').strip()

    args = [
        'docker', 'exec', '-ti',
        '--env', 'COLORFGBG',
        '--env', 'TERM',
        '-u', user,
        name,
        'bash', '-li',
    ]

    if cmd:
        args.extend(['-c', cmd])

    print('Entering {} with following images:'.format(name))
    print_image_matrix(name)
    run(args, check=False)


def docker_run(name, image, home, addargs=None, debug=None, volume_images=None):
    # pylint: disable=too-many-arguments,too-many-locals

    user = shellout('id -un').strip()
    user_id = int(shellout('id -u').strip())
    group = shellout('id -gn').strip()
    group_id = int(shellout('id -g').strip())
    video_group_id = int(shellout('getent group video |cut -d: -f3').strip())

    cmd = [
        'docker', 'run',
        '-h', name,
        '--detach',
        '--name', name,
        '--env', 'COLORFGBG',
        '--env', 'DISPLAY',
        '--env', 'EMAIL',
        '--env', 'GIT_AUTHOR_EMAIL',
        '--env', 'GIT_AUTHOR_NAME',
        '--env', 'GIT_COMMITTER_EMAIL',
        '--env', 'GIT_COMMITTER_NAME',
        '--env', 'SSH_AUTH_SOCK',
        '--env', 'TERM',
        '--env', 'TIMEZONE={}'.format(get_timezone()),
        '--env', 'USER={}'.format(user),
        '--env', 'GROUP={}'.format(group),
        '--env', 'USER_ID={}'.format(user_id),
        '--env', 'GROUP_ID={}'.format(group_id),
        '--env', 'VIDEO_GROUP_ID={}'.format(video_group_id),
        '-v', '/dev/dri:/dev/dri',
        '-v', '/dev/shm:/dev/shm',
        '-v', '/tmp/.X11-unix:/tmp/.X11-unix',
        '-v', '{}:/home/{}'.format(home.resolve(), user),
        '--label', 'ade_version={}'.format(VERSION),
    ]

    dotssh = home / '.ssh'
    try:
        os.mkdir(str(dotssh))
    except FileExistsError:
        pass
    else:
        (dotssh / 'WILL_BE_MOUNTED_FROM_OUTSIDE').write_text('')
    cmd.extend(['-v', '{}/.ssh:/home/{}/.ssh'.format(os.environ['HOME'], user)])

    if os.environ.get('SSH_AUTH_SOCK'):
        cmd.extend(['-v', '{x}:{x}'.format(x=os.environ.get('SSH_AUTH_SOCK'))])

    if debug:
        cmd.extend(['--env', 'DEBUG=1'])

    images = [image]
    images.extend(volume_images or ())
    cmd.extend(['--label', 'ade_images={}'.format(json.dumps([x.fqn for x in images]))])

    volumes_from = []
    for img in volume_images or ():
        container = make_container(envname=name, image=img)
        cmd.extend(['--volumes-from', '{}:ro'.format(container)])
        volumes_from.append(container)
    cmd.extend(['--label', 'ade_volumes_from={}'.format(json.dumps(volumes_from))])

    if addargs:
        cmd.extend(addargs)

    cmd.append(image.fqn)
    did = runout(cmd).strip()

    if os.environ.get('DISPLAY'):
        hostname = runout(['docker', 'inspect', "--format='{{ .Config.Hostname }}'", did])
        cp = shell("xhost +local:{}".format(hostname), check=False)
        if cp.returncode != 0:
            print("WARNING: Could not find xhost, you won't be able to launch X applications")

    logtail = Popen(['docker', 'logs', '-f', name], stdout=PIPE)
    line = None
    while line != 'ADE startup completed.':
        line = logtail.stdout.readline().decode('utf-8')
        if not line:
            break
        line = line.rstrip()
        print(line)
    else:
        return True
    return False


def docker_stop(name):
    containers = [name]
    containers.extend(get_label(name, 'ade_volumes_from'))
    for container in containers:
        print('Stopping', container)
        run(['docker', 'stop', '-t', '0', container], stdout=DEVNULL, stderr=DEVNULL, check=False)


def get_label(name, key):
    """Get label for key from specific container."""
    label = runout(['docker', 'inspect', '--format', '{{json .Config.Labels}}', name])
    return json.loads(json.loads(label)[key])


def is_running(name):
    """Check if specific container is running"""
    return name in shellout("docker ps --format '{{.Names}}'").split()


def make_container(envname, image, recreate=None):
    """Create container for image."""
    fqn = image.fqn
    name = '{}_{}'.format(envname, fqn.replace('/', '_').replace(':', '_'))

    if recreate:
        run(['docker', 'rm', '--force', '--volumes', name],
            check=False, stdout=DEVNULL, stderr=DEVNULL)
        existing = ()
    else:
        existing = shellout("docker ps -a --format '{{.Names}}'").split()

    if name not in existing:
        print('Creating volume container for', fqn)
        cmd = ['docker', 'run', '--label', 'ade_version={}'.format(VERSION),
               '--read-only', '--detach', '--name', name, fqn]
        try:
            run(cmd, stdout=DEVNULL, stderr=DEVNULL)
        except CalledProcessError as e:
            login(image)
            run(cmd, stdout=DEVNULL, check=exit)
    else:
        run(['docker', 'start', name])

    return name


def print_image_matrix(name, images=None):
    """Print images used by container."""
    images = images or [Image(x) for x in get_label(name, 'ade_images')]
    matrix = [(x.name, x.tag, x.fqn) for x in images]
    aligns = [max([len(x) for x in col]) for col in zip(*matrix)]
    for line in matrix:
        fmt = ' | '.join(['{:%s}' % x for x in aligns])
        print(fmt.format(*line))


async def update(envname, images):
    for img in images:
        try:
            if await update_image(img):
                make_container(envname=envname, image=img, recreate=True)
        except CalledProcessError as e:
            print(str(e), file=sys.stderr)
            sys.exit(e.returncode)
