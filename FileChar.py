__author__ = 'Fitz'

import mutants.Space
import mutants.Wall
import mutants.Door
import mutants.ExteriorSpace
import mutants.Equipment
import mutants.Mutant

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
    >>> eq1 = fc.getEquipment("=")
    >>> eq1.name
    'Pistol'
    >>> eq2 = fc.getEquipment("!")
    >>> eq2.handtohandadd
    3
    >>> eq3 = fc.getEquipment("Y")
    >>> if (eq3 == None): print("None, as expected")
    None, as expected
    """

    def __init__(self):
        self.BoardCharLookup = {
            "#": ("Wall", mutants.Wall.Wall),
            "D": ("Door", mutants.Door.Door),
            " ": ("Space", mutants.Space.Space),
            "-": ("ExteriorSpace", mutants.ExteriorSpace.ExteriorSpace)
        }

        # attributes: H2H add, ranged damage, range, healing
        self.EquipCharLookup = {
            ">": ("Rifle",  2, 7, 10, 0),
            "=": ("Pistol", 1, 6, 4, 0),
            "x": ("Axe", 7, 0, 0, 0, 0),
            "~": ("Extinguisher", 2, 1, 2, 0),
            "+": ("FirstAid", 1, 0, 0, 3),
            "*": ("Shotgun", 2, 9, 3, 0),
            "!": ("Bat", 3, 0, 0, 0),
            "|": ("Pipe", 4, 0, 0, 0),
            "^": ("SpareParts", 0, 0, 0, 0)
        }

    def getTerrain(self, boardchar):
        ty = self.BoardCharLookup[boardchar][1]
        terr = ty()
        return(terr)

    def getEquipment(self, boardchar):
        nm = None
        if boardchar in self.EquipCharLookup:
            nm = self.EquipCharLookup[boardchar][0]
            hth = self.EquipCharLookup[boardchar][1]
            rnga = self.EquipCharLookup[boardchar][2]
            rng = self.EquipCharLookup[boardchar][3]
            heal = self.EquipCharLookup[boardchar][4]
        if (nm == None):
            equip = None
        else:
            equip = mutants.Equipment.Equipment(nm, nm, hth, rnga, rng, heal)
        return(equip)

    def getMutant(self, boardchar):
        m = None
        if boardchar == "M":
            m = mutants.Mutant.Mutant()
        return (m)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
