
class Star:

    def __init__(self, x, y, index):
        self.x = x
        self.y = y
        self.owner = None # either None or number >= 0
        self.index = index