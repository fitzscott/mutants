__author__ = 'Fitz'

import mutants.MovingPiece

class Human(mutants.MovingPiece.MovingPiece):
    """
    The human pieces on the board are the basis of the victory conditions.
    >>> bart = Human("Bart", "Bart", 4, 6, 6)
    >>> molly = Human("Molly", "Molly", 6, 5, 4)
    >>> charlie = Human("Charlie", "Charlie", 7, 3, 2)
    """
    def __init__(self, name, image, movePts, hitPts, h2h):
        super().__init__(name, image, movePts, hitPts)
        self.handtohand = h2h

