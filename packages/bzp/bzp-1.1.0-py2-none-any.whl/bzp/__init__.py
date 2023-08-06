import os.path as op
import bz2
import pickle


def get_bzppath(dst):
    _, ext = op.splitext(dst)
    if ext != '.bzp':
        dst += '.bzp'
    return dst


def dump(content, dst):
    with bz2.BZ2File(get_bzppath(dst), 'w') as f:
        pickle.dump(content, f)

def load(dst):
    with bz2.BZ2File(get_bzppath(dst), 'r') as f:
        return pickle.load(f)
