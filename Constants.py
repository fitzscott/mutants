__author__ = 'Fitz'

class Constants:
    # directions
    UP = (0, -1)
    DOWN = (0, +1)
    LEFT = (-1, 0)
    RIGHT = (+1, 0)

    dirStrings = ["Up", "Down", "Left", "Right", "None"]

    WINSIZE = (800, 600)

    IMAGESIDESIZE = 20

    MUTANTSPERWAVE = [60, 80, 100]
    MAXMUTANTEYESIGHT = 10
    MAXMUTANTSQUAREMEM = 30

    NUMROBOTS = 10

    GAMEBOARD = "testboard5"

    # attributes:  movement, hit points, hand-to-hand, ranged
    playerpieceattributes = {
        "Bart": (4, 6, 6, 4),
        "Molly": (6, 5, 4, 7),
        "Charlie": (7, 3, 2, 4),
        "Professor": (3, 3, 2, 4),
        "Robot": (3, 3, 3, 5)
    }
