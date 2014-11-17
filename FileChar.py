__author__ = 'Fitz'

import mutants.Space
import mutants.Wall
import mutants.Door

class FileChar():
    """
    Translate characters from board file into terrain
    >>> fc = FileChar()
    >>> ty = fc.BoardCharLookup[" "][1]
    >>> strrep = fc.BoardCharLookup[" "][0]
    >>> print(strrep)
    Space
    >>> newSpc = ty()
    >>> print(newSpc.name)
    Space
    >>> if (newSpc.getmovethru()): print("Can move through space")
    Can move through space
    >>> ty2 = fc.getTerrain("D")
    >>> ty2.name
    'Door'
    """

    def __init__(self):
        self.BoardCharLookup = { "#": ("Wall", mutants.Wall.Wall),
                                 "D": ("Door", mutants.Door.Door),
                                 " ": ("Space", mutants.Space.Space)}

    def getTerrain(self, boardchar):
        ty = self.BoardCharLookup[boardchar][1]
        terr = ty()
        return(terr)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
