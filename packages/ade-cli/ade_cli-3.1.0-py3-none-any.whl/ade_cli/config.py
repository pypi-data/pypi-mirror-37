# -*- coding: utf-8 -*-
#
# Copyright 2018  Ternaris.
# SPDX-License-Identifier: Apache-2.0

import os
from pathlib import Path

from .registry import Image
from .utils import find_file


class Config:
    def __init__(self, debug, home, images, name, gitlab, registry, runargs):
        self.debug = debug
        self.home = home
        self.images = images
        self.name = name
        self.gitlab = gitlab
        self.registry = registry
        self.runargs = runargs


def load_config():
    home = os.environ.get('ADE_HOME', find_file('.adehome', parent=True))
    cfg = Config(**{
        'debug': os.environ.get('ADE_DEBUG'),
        'home': Path(home) if home else None,
        'images': [Image(x) for x in os.environ.get('ADE_IMAGES', '').split()],
        'name': os.environ.get('ADE_NAME', 'ade'),
        'gitlab': os.environ.get('ADE_GITLAB'),
        'registry': os.environ.get('ADE_REGISTRY'),
        'runargs': tuple(os.environ.get('ADE_DOCKER_RUN_ARGS', '').split()),
    })
    return cfg
