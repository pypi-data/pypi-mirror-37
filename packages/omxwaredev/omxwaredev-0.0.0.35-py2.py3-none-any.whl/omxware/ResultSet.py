

class ResultSet(list):
    def __init__(self, callingFn):
        self._hasnext = False

    def __getitem__(self, key):
        return super(ResultSet, self).__getitem__(key - 1)

