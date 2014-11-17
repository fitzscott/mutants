__author__ = 'Fitz'

import os
import pygame, sys
from pygame.locals import *
import mutants.Constants
import mutants.BoardFile

class Display():
    """
    Handle displaying the board and the pieces, as well as any
    messages for the player.
    >>> d = Display()
    >>> d.loadResources("testboard1")
    """

    def __init__(self):
        self.__screen = pygame.display.set_mode(mutants.Constants.Constants.WINSIZE, pygame.DOUBLEBUF)
        pygame.display.set_caption("Attack of the Mutants")
        self.__clock = pygame.time.Clock()
        pygame.mouse.set_visible(0)
        self.__images = {}
        self.__board = None

    def loadBoard(self, flnm):
        bf = mutants.BoardFile.BoardFile()
        bf.readFromFile(flnm)
        self.__board = bf.createBoard()

    def loadImage(self, cwd, typestr):
        flnm = os.path.join(cwd, "Resources", "Images", typestr + ".png")
        #print("Loading image file " + flnm)
        img = pygame.image.load(flnm)
        self.__images[typestr] = img

    def loadResources(self, boardname):
        cwd = os.getcwd()
        self.loadImage(cwd, "Door")
        self.loadImage(cwd, "Space")
        self.loadImage(cwd, "Wall")
        self.loadImage(cwd, "ExteriorSpace")
        self.loadImage(cwd, "SmashedDoor")
        self.loadImage(cwd, "Axe")
        self.loadImage(cwd, "Bat")
        self.loadImage(cwd, "Extinguisher")
        self.loadImage(cwd, "FirstAid")
        self.loadImage(cwd, "Pipe")
        self.loadImage(cwd, "Pistol")
        self.loadImage(cwd, "Rifle")
        self.loadImage(cwd, "Shotgun")
        self.loadImage(cwd, "SpareParts")
        self.loadBoard(boardname)

    def runLoop(self):
        while (1):
            self.__clock.tick(40)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self.__screen.fill((191, 191, 191))
            for row in range(self.__board.height):
                for col in range(self.__board.width):
                    #print("Row is " + str(row) + ", col is " + str(col))
                    equip = self.__board.getSquare(col, row).getequipment()
                    if (equip == None):
                        imgnm = self.__board.getSquare(col, row).getTerrain().name
                    else:
                        imgnm = equip.name
                    img = self.__images[imgnm]
                    self.__screen.blit(img, (col * mutants.Constants.Constants.IMAGESIDESIZE,
                                             row * mutants.Constants.Constants.IMAGESIDESIZE))
            pygame.display.update()

    def runLoopTest(self):
       img1 = pygame.image.load(r"C:\Users\Fitz\Pictures\mut1.png")
       self.__screen.fill((127, 127, 127))
       while (1):
            self.__clock.tick(40)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self.__screen.blit(self.__images["Door"], (0, 0))
            self.__screen.blit(self.__images["Wall"], (40, 40))
            self.__screen.blit(self.__images["Space"], (80, 80))

            x, y = pygame.mouse.get_pos()
            self.__screen.blit(img1, (x, y))
            pygame.display.update()

if __name__ == "__main__":
    import doctest
    doctest.testmod()




