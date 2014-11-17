__author__ = 'Fitz'

class Terrain():
    """
    Represents underlying terrain on the board - empty space, a door, a wall, etc.
    >>> t = Terrain("Door", None)
    >>> if (not t.getmovethru()): print("Can't move thru")
    Can't move thru
    """

    def __init__(self, name, image):
        self.__name = name
        self.__image = image
        self.__moveThru = False

    @property
    def name(self):
        return(self.__name)

    @name.setter
    def name(self, name):
        self.__name = name

    def getmovethru(self):
        return(self.__moveThru)

    def setmovethru(self, boolval):
        self.__moveThru = boolval

    def movethru(self, piece):
        return (self.__moveThru)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
