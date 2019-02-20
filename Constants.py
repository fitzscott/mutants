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
    #MUTANTSPERWAVE = [10, 20, 30]
    #MUTANTSPERWAVE = [3, 3, 100]
    MAXMUTANTEYESIGHT = 10
    MAXMUTANTSQUAREMEM = 30

    NUMROBOTS = 10

    GAMEBOARD = "Board3"
    NUMBOARDS = 6
    NUMMUTANTNAMESPERSEX = 200

    # attributes:  movement, hit points, hand-to-hand, ranged
    playerpieceattributes = {
        "Buck":      (4, 12, 5, 4),
        "Molly":     (6, 9, 3, 7),
        "Charlie":   (7, 7, 2, 4),
        "Jeb":       (5, 10, 4, 4),
        "Professor": (3, 7, 1, 3),
        "Robot":     (3, 4, 2, 2),
        "Computer":  (0, 7, 0, 0)
    }

    TOHIT = 8
