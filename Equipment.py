__author__ = 'Fitz'

import mutants.Piece

class Equipment(mutants.Piece.Piece):
    """
    Represents tools & equipment, including weapons - rifles, pistols, axes, pipes, etc. -
    as well as tools - first aid kits, repair kits (first aid for robots), slide rule (?),
    spare parts (for building robots), etc.
    These are all guesses - will refine later.
    >>> rifle = Equipment("Rifle", "Rifle", 2, 7, 10, 0)
    >>> pistol = Equipment("Pistol", "Pistol", 1, 6, 4, 0)
    >>> shotgun = Equipment("Shotgun", "Shotgun", 2, 9, 3, 0)
    >>> bat = Equipment("Bat", "Bat", 3)
    >>> axe = Equipment("Axe", "Axe", 7)
    >>> extinguisher = Equipment("Extinguisher", "Extinguisher", 2, 1, 2, 0)
    >>> firstaidkit = Equipment("FirstAid", "FirstAid", 1, 0, 0, 3)
    >>> print(firstaidkit.name + " heals for " + str(firstaidkit.heals))
    FirstAid heals for 3
    >>> print(shotgun.name + " shoots to range " + str(shotgun.effectiverange) + \
            " for " + str(shotgun.rangedattack) + " damage.")
    Shotgun shoots to range 3 for 9 damage.
    >>> print(axe.name + " hacks for " + str(axe.handtohandadd) + " additional damage")
    Axe hacks for 7 additional damage
    """

    def __init__(self, name, image, h2hatt, rangatt=0, effrange=0, heal=0):
        super().__init__(name, image)
        self.__handtohandadd = h2hatt
        self.__rangedattack = rangatt
        self.__effectiverange = effrange
        self.__healpts = heal

    @property
    def handtohandadd(self):
        return(self.__handtohandadd)

    @property
    def rangedattack(self):
        return(self.__rangedattack)

    @property
    def effectiverange(self):
        return(self.__effectiverange)

    @property
    def heals(self):
        return(self.__healpts)

if __name__ == "__main__":
    import doctest
    doctest.testmod()

