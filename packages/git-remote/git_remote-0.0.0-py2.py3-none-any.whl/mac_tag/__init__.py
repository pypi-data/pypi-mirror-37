#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from public import public
import runcmd
import this_is
import values

"""
https://github.com/jdberry/tag
"""

bin = "/usr/local/bin/tag"


def run(args):
    if not os.path.exists(bin):
        raise OSError("%s NOT EXISTS\nrun `brew install tag`" % bin)
    return runcmd.run([bin] + values.get(args))._raise().out


def _tags(value):
    if not value:
        return []
    if this_is.string(value):
        return [value]
    return [",".join(value)]


@public
def add(tags, path):
    if path:
        run(["-a"] + _tags(tags) + values.get(path))


@public
def remove(tags, path):
    if not tags:
        tags = "*"  # remove all tags by default
    if path:
        run(["-r"] + _tags(tags) + values.get(path))


@public
def set(tags, path):
    if path:
        run(["-s"] + _tags(tags) + values.get(path))


@public
def match(tags, path=None):
    args = ["-m"] + _tags(tags) + values.get(path)
    out = run(args)
    return out.splitlines()


@public
def parse_list_output(out):
    result = dict()
    for l in out.splitlines():
        if "\t" in l:
            path, tags = l.split("\t")
            result[path] = tags.split(",")
        else:
            result[l] = []
    return result


@public
def list(path):
    args = ["-l"] + values.get(path)
    out = run(args)
    return parse_list_output(out)


@public
def find(tags, path=None):
    args = ["-f"] + _tags(tags) + values.get(path)
    out = run(args)
    return out.splitlines()
