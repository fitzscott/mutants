__author__ = 'Fitz'

import Terrain as trr

class Space(trr.Terrain):
    """
    Empty space terrain on the board - easy to move through
    >>> sp = Space()
    >>> if (sp.getmovethru()): print("Can move through space")
    Can move through space
    """

    def __init__(self):
        super().__init__("Space", "Space")
        self.setmovethru(True)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
