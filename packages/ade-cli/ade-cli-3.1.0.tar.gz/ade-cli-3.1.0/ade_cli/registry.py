# -*- coding: utf-8 -*-
#
# Copyright 2017 - 2018  Ternaris.
# SPDX-License-Identifier: Apache-2.0

"""Communicate with docker registry"""

import asyncio
from subprocess import CalledProcessError, DEVNULL, PIPE

import aiohttp

from .credentials import get_credentials
from .utils import run


class NoSuchImage(Exception):
    """Requested image is not available"""


class NoSuchTag(Exception):
    """Requested tag does not exist for image.

    raise NoSuchTag(img, tag, available_tags)
    """


class TokenError(Exception):
    """Error obtaining token for URL. Auth data is wrong"""


class Image:
    """Data model for an image in a docker registry."""
    registry = None
    namespace = None
    name = None
    tag = None

    @property
    def fqn(self):
        """Fully qualified name of a docker image including the tag"""
        fmt = '{registry}/{namespace}/{name}:{tag}' if self.registry else '{name}:{tag}'
        return fmt.format(**self.__dict__)

    @property
    def api_url(self):
        """URL for API of the image's registry"""
        return 'https://{registry}/v2'.format(**self.__dict__) if self.registry else None

    @property
    def tags_url(self):
        """URL for API endpoint for list of tags for image"""
        return 'https://{registry}/v2/{namespace}/{name}/tags/list'.format(**self.__dict__) \
            if self.registry else None

    def __init__(self, fqn):
        try:
            rest, self.tag = fqn.split(':')
        except ValueError:
            self.tag = 'latest'
            rest = fqn

        components = rest.split('/')
        if len(components) == 1:
            self.name = components[0]
            return

        self.registry = components.pop(0)
        self.name = components.pop()
        self.namespace = '/'.join(components)

    def __repr__(self):
        return "Image('{}')".format(self.fqn)


async def adjust_tag(client, image, selectors):
    """Adjust image tag according to selectors and availability"""
    tags = await get_tags(client, image)
    for name, tag in selectors:
        if image.name == name:
            if tag not in tags:
                raise NoSuchTag(image, tag, sorted(tags))
            image.tag = tag
            break
        if name is None and tag in tags:
            image.tag = tag
            break


async def adjust_tags(images, selectors):
    """Adjust tags of images according to selectors and availability"""
    async with aiohttp.ClientSession() as client:
        reqs = [adjust_tag(client, img, selectors) for img in images]
        await asyncio.gather(*reqs)


async def get(client, url, registry, accept=None, stream=False):
    """Get url, implicitly handling authentication"""
    headers = {}
    accept = accept or 'application/json'
    if accept:
        headers['Accept'] = accept

    resp = await client.get(url, headers=headers)
    if resp.status == 401:
        token = await _authtoken(client, resp.headers, registry)
        headers['Authorization'] = 'Bearer {}'.format(token)
        resp = await client.get(url, headers=headers)

    if stream:
        return resp.content
    return await resp.json(content_type=accept)


def login(img):
    """Login into registry serving image"""
    username, token = get_credentials(img.registry).values()
    run(['docker', 'login', '--username', username, '--password-stdin', img.registry],
        input=token.encode('utf-8'))


async def update_image(img):
    """Update an image from docker registry"""
    try:
        old_id = run(['docker', 'image', 'inspect', '--format', '{{.Id}}', img.fqn],
                     stdout=PIPE, stderr=DEVNULL).stdout.decode('utf-8').strip()
    except CalledProcessError:
        old_id = None

    try:
        run(['docker', 'pull', img.fqn])
    except CalledProcessError:
        login(img)
        run(['docker', 'pull', img.fqn])

    new_id = run(['docker', 'image', 'inspect', '--format', '{{.Id}}', img.fqn],
                 stdout=PIPE).stdout.decode('utf-8').strip()
    return new_id != old_id


async def get_tags(client, image):
    """Get list of tags for image from registry"""
    data = await get(client, image.tags_url, registry=image.registry)
    try:
        return [x for x in data['tags'] if not x.startswith('commit-')]
    except KeyError:
        raise NoSuchImage(image)


async def _authtoken(client, headers, registry):
    info = {
        k: v.split('"')[1] for k, v in [
            x.split('=') for x in headers['Www-Authenticate'].split()[1].split(',')
        ]
    }
    info['client_id'] = 'ade'
    auth = aiohttp.BasicAuth(*get_credentials(registry).values())
    resp = await client.get(info.pop('realm'), auth=auth, params=info)
    resp = await resp.json()
    try:
        token = resp['token']
    except KeyError:
        raise TokenError()
    return token
