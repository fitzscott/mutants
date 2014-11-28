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

        # attributes: H2H hit bonus, H2H damage bonus, ranged bonus, ranged damage, range, healing
        self.EquipCharLookup = {
            ">": ("Rifle",        2, 2, 4, 7, 10, 0),
            "=": ("Pistol",       1, 1, 2, 6, 6, 0),
            "x": ("Axe",          3, 7, 0, 0, 0, 0),
            "~": ("Extinguisher", 2, 2, 0, 1, 2, 0),
            "+": ("FirstAid",     0, 1, 0, 0, 0, 3),
            "*": ("Shotgun",      2, 2, 4, 9, 4, 0),
            "!": ("Bat",          4, 3, 0, 0, 0, 0),
            "|": ("Pipe",         4, 4, 0, 0, 0, 0),
            "^": ("SpareParts",   0, 0, 0, 0, 0, 0)
        }

    def getTerrain(self, boardchar):
        ty = self.BoardCharLookup[boardchar][1]
        terr = ty()
        return(terr)

    def getEquipment(self, boardchar):
        nm = None
        if boardchar in self.EquipCharLookup:
            nm = self.EquipCharLookup[boardchar][0]
            hth_hit = self.EquipCharLookup[boardchar][1]
            hth_dam = self.EquipCharLookup[boardchar][2]
            rng_hit = self.EquipCharLookup[boardchar][3]
            rng_dam = self.EquipCharLookup[boardchar][4]
            rng = self.EquipCharLookup[boardchar][5]
            heal = self.EquipCharLookup[boardchar][6]
        if (nm == None):
            equip = None
        else:
            equip = mutants.Equipment.Equipment(nm, nm, hth_hit, hth_dam, rng_hit, rng_dam, rng, heal)
        return(equip)

    def getMutant(self, boardchar):
        m = None
        if boardchar == "M":
            m = mutants.Mutant.Mutant()
        return (m)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
