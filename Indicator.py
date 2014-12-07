__author__ = 'Fitz'

class Indicator():
    """
    Indicates when something has happened in a location.  When a human character dies, it's a tombstone.
    When a robot is destroyed, it's some parts (maybe).  Only lasts for a bit on-screen.
    """
    def __init__(self, name, image, prevname):
        self.__name = name
        self.__image = image
        self.__represents = prevname

    @property
    def image(self):
        return (self.__image)

    @image.setter
    def image(self, img):
        self.__image = img

    @property
    def name(self):
        return(self.__name + " for " + self.__represents)

    @name.setter
    def name(self, nm):
        self.__name = nm


