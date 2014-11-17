__author__ = 'Fitz'

import mutants.Space

class ExteriorSpace(mutants.Space.Space):
    """
    Exterior space - outside the building, where the mutants arrive.
    >>> sp = ExteriorSpace()
    >>> if (sp.getmovethru()): print("Can move through space")
    Can move through space
    """

    def __init__(self):
        super().__init__()
        self.name = "ExteriorSpace"
        self.image = "ExteriorSpace"

if __name__ == "__main__":
    import doctest
    doctest.testmod()

