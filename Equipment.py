__author__ = 'Fitz'

import mutants.Piece

class Equipment(mutants.Piece.Piece):
    """
    Represents tools & equipment, including weapons - rifles, pistols, axes, pipes, etc. -
    as well as tools - first aid kits, repair kits (first aid for robots), slide rule (?),
    spare parts (for building robots), etc.
    >>> shotgun = Equipment("Shotgun", "Shotgun", 2, 2, 4, 9, 4, 0)
    >>> extinguisher = Equipment("Extinguisher", "Extinguisher", 2, 1, 2, 0)
    >>> firstaidkit = Equipment("FirstAid", "FirstAid", 0, 1, 0, 0, 0, 3)
    >>> print(firstaidkit.name + " heals for " + str(firstaidkit.heals))
    FirstAid heals for 3
    >>> print(shotgun.name + " shoots to range " + str(shotgun.effectiverange) + \
            " for " + str(shotgun.rangeddamage) + " damage.")
    Shotgun shoots to range 4 for 9 damage.
    >>> axe = Equipment("Axe", "Axe", 3, 7, 0, 0, 0, 0)
    >>> print(axe.name + " hacks for " + str(axe.handtohanddamagebonus) + " additional damage")
    Axe hacks for 7 additional damage
    """

    # attributes: H2H hit bonus, H2H damage bonus, ranged bonus, ranged damage, range, healing
    def __init__(self, name, image, h2hhit=0, h2hdam=0, rnghit=0, rngdam=0, effrange=0, heal=0):
        super().__init__(name, image)
        self.__handtohandhitadd = h2hhit
        self.__handtohanddamageadd = h2hdam
        self.__rangedhitadd = rnghit
        self.__rangeddamage = rngdam
        self.__effectiverange = effrange
        self.__healpts = heal

    @property
    def handtohandhitbonus(self):
        return (self.__handtohandhitadd)

    @property
    def handtohanddamagebonus(self):
        return (self.__handtohanddamageadd)

    @property
    def rangedhitbonus(self):
        return (self.__rangedhitadd)

    @property
    def rangeddamage(self):
        return (self.__rangeddamage)

    @property
    def effectiverange(self):
        return(self.__effectiverange)

    @property
    def heals(self):
        return(self.__healpts)

if __name__ == "__main__":
    import doctest
    doctest.testmod()

