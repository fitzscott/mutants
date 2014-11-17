__author__ = 'Fitz'

import mutants.Terrain

class Wall(mutants.Terrain.Terrain):
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
