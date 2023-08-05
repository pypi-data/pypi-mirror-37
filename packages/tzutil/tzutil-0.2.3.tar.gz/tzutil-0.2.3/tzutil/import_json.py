from os.path import join
from json import load, dump


class ImportJson:

    def __init__(self, root):
        self.root = root

    def __call__(self, path, data=None):
        fpath = join(self.root, path + ".json")
        if data is None:
            with open(fpath) as f:
                r = load(f)
                return r
        else:
            with open(fpath, "w") as f:
                dump(data, f)
