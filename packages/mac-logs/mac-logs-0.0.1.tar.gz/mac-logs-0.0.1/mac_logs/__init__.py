#!/usr/bin/env python
import os
import find
import public
import mac_colors

"""
~/Library/Logs
"""

PATH = os.path.join(os.environ["HOME"], "Library/Logs")


def _size(path):
    return os.stat(path).st_size


def files(filenames=None, minsize=0):
    if not minsize:
        minsize = 0
    if not os.path.exists(PATH):
        return
    for f in find.files(PATH):
        if _size(f) >= minsize and (not filenames or os.path.basename(f) in filenames):
            yield f


@public.add
def logs(filenames=None, minsize=0):
    return list(filter(lambda f: f[-4:] == ".log", files(filenames, minsize)))


@public.add
def rm(filenames=None, minsize=0):
    for f in logs(filenames, minsize):
        if os.path.exists(f):
            os.unlink(f)


@public.add
def errors():
    result = []
    for f in logs(minsize=1):
        if "err" in os.path.splitext(os.path.basename(f))[0]:
            result.append(f)
    return result


def _trees(paths):
    for path in paths:
        while path != os.path.dirname(PATH):
            yield path
            path = os.path.dirname(path)


@public.add
def tag():
    red = list(_trees(errors()))
    none = list(set(_trees(logs())) - set(red))
    mac_colors.red(red)
    mac_colors.none(none)
