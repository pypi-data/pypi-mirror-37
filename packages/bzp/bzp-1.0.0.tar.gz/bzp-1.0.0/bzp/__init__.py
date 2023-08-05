import bz2
import pickle


def dump(content, dst):
    with bz2.BZ2File(dst, 'w') as f:
        pickle.dump(content, f)

def load(dst):
    with bz2.BZ2File(dst, 'r') as f:
        return pickle.load(f)
