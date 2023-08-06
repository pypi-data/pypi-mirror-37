#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import public
import runcmd
import values

"""
https://github.com/jdberry/tag
"""

bin = "/usr/local/bin/tag"


@public.add
def run(args):
    if not os.path.exists("/usr/local/bin/tag"):
        raise OSError("""/usr/local/bin/tag NOT INSTALLED

https://github.com/jdberry/tag
brew install tag
""")
    args = ["/usr/local/bin/tag"] + list(args)
    return runcmd.run(args)._raise().out


@public.add
def replace(tags, path):
    args = ["-s", ",".join(tags)] + values.get(path)
    run(args)


@public.add
def none(path):
    replace(["none"], path)


@public.add
def blue(path):
    replace(["blue"], path)


@public.add
def gray(path):
    replace(["gray"], path)


@public.add
def grey(path):
    replace(["gray"], path)


@public.add
def green(path):
    replace(["green"], path)


@public.add
def orange(path):
    replace(["orange"], path)


@public.add
def red(path):
    replace(["red"], path)


@public.add
def purple(path):
    replace(["purple"], path)


@public.add
def yellow(path):
    replace(["yellow"], path)


@public.add
def get(path):
    args = ["-l"] + values.get(path)
    out = run(args)
    result = dict()
    for l in out.splitlines():
        if "\t" in l:
            path, tags = l.split("\t")
            result[path] = tags.split(",")
        else:
            result[l] = []
    return result

