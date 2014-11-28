__author__ = 'Fitz'

class Constants:
    # directions
    UP = (0, -1)
    DOWN = (0, +1)
    LEFT = (-1, 0)
    RIGHT = (+1, 0)

    directions = [UP, DOWN, LEFT, RIGHT]

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
        "Bart":      (4, 12, 4, 4),
        "Molly":     (6, 9, 2, 7),
        "Charlie":   (7, 7, 2, 4),
        "Professor": (3, 7, 1, 4),
        "Robot":     (3, 6, 2, 5)
    }

    TOHIT = 8
