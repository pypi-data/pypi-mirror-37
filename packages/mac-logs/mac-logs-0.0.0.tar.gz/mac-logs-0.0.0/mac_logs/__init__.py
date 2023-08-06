#!/usr/bin/env python
import os
import find
import public

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
