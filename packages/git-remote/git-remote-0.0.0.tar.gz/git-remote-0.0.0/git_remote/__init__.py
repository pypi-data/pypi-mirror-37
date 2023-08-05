#!/usr/bin/env python
import runcmd
from public import public

"""
https://git-scm.com/docs/git-remote
"""


@public
def run(args):
    return runcmd.run(["git", "remote"] + list(args))._raise().out


@public
def add(name, url):
    run(["add", name, url])


@public
def remove(name):
    run(["remove", name])


@public
def rm(name):
    run(["rm", name])


@public
def rename(old, new):
    run(["rename", old, new])


@public
def set_url(name, url):
    return run(["set-url", name, url])


@public
def remotes():
    result = []
    for l in run(["-v"]).splitlines():
        name, url_role = l.split("\t")
        url, role = url_role.split(" ")
        if "fetch" in role:
            result.append([name, url])
    return result


@public
def names():
    return list(lambda name, url: name, remotes())


@public
def urls():
    return list(lambda name, url: url, remotes())
