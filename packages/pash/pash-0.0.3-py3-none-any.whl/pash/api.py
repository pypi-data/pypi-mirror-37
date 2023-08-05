import os
from collections import namedtuple
from .ls_class import LS

path = os.getcwd()


def ls(path=path, sort_by_size=False,
        list_subdir=False, show_hidden=False,
        long_format=False):
    Args = namedtuple(
        'Args',
        'path, sort_by_size, list_subdir, ' +
        'show_hidden, long_format')
    args = Args(
        path, sort_by_size, list_subdir,
        show_hidden, long_format)
    ls = LS(args)
    ls.get_and_display()
