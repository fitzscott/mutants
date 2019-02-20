__author__ = 'Fitz'

import Terrain as tr

class Wall(tr.Terrain):
    """
    Represents a wall.  No cats who can walk through walls in this game.
    >>> w = Wall()
    >>> if (not w.getmovethru()): print("Of course you can't walk through walls.")
    Of course you can't walk through walls.
    """

    def __init__(self):
        super().__init__("Wall", "Wall")

if __name__ == "__main__":
    import doctest
    doctest.testmod()
