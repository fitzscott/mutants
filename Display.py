__author__ = 'Fitz'

import os
import pygame, sys
from pygame.locals import *
import mutants.Constants
import mutants.BoardFile
import mutants.Game
import mutants.PlayerPiece

class Display():
    """
    Handle displaying the board and the pieces, as well as any
    messages for the player.
    >>> d = Display(None)
    >>> d.loadResources("testboard1")
    """

    def __init__(self, game):
        self.__screen = pygame.display.set_mode(mutants.Constants.Constants.WINSIZE, pygame.DOUBLEBUF)
        pygame.display.set_caption("Attack of the Mutants")
        self.__clock = pygame.time.Clock()
        #pygame.mouse.set_visible(0)
        self.__images = {}
        self.__board = None
        self.__game = game

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
        self.loadImage(cwd, "Molly")
        self.loadImage(cwd, "Bart")
        self.loadImage(cwd, "Charlie")
        self.loadImage(cwd, "Robot")
        self.loadImage(cwd, "Mutant")
        self.loadBoard(boardname)

    @property
    def board(self):
        return(self.__board)

    def runLoop(self, maxtix=10000000):
        i = 0
        drawwhiterect = False
        while (i < maxtix):
            self.__clock.tick(40)
            self.__screen.fill((191, 191, 191))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    col = x // mutants.Constants.Constants.IMAGESIDESIZE
                    row = y // mutants.Constants.Constants.IMAGESIDESIZE
                    sq = self.__board.getSquare(col, row)
                    if (sq != None):
                        if (sq.isOccupied()):
                            if pygame.mouse.get_pressed()[0]:
                                occupant = sq.piece
                                #print(str(type(occupant)))
                                if issubclass(type(occupant), mutants.PlayerPiece.PlayerPiece):
                                    self.__game.clearfoci()
                                    occupant.focus = True
                                    #print(occupant.name + " has focus at (" + str(col) + ", " + str(row) + ").")
                            elif pygame.mouse.get_pressed()[2]:    # right-click?
                                activepiece = self.__game.piecewithfocus()
                                if activepiece != None:
                                    activepiece.attack(sq)
                    else:
                        self.__game.mutantturn = True
                        self.__game.nextturn()

                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    col = x // mutants.Constants.Constants.IMAGESIDESIZE
                    row = y // mutants.Constants.Constants.IMAGESIDESIZE
                    sq = self.__board.getSquare(col, row)
                    if not self.__game.movepiecewithfocus(sq):
                        print("Cannot move that piece to (" + str(col) + ", " + str(row) + ").")
                    drawwhiterect = False

                if event.type == pygame.MOUSEMOTION:
                    if pygame.mouse.get_pressed()[0]:
                        drawwhiterect = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if not self.__game.movepiecewithfocus(None, mutants.Constants.Constants.UP):
                            print("Cannot move that piece upward.")
                    if event.key == pygame.K_DOWN:
                        if not self.__game.movepiecewithfocus(None, mutants.Constants.Constants.DOWN):
                            print("Cannot move that piece downward.")
                    if event.key == pygame.K_LEFT:
                        if not self.__game.movepiecewithfocus(None, mutants.Constants.Constants.LEFT):
                            print("Cannot move that piece to the left.")
                    if event.key == pygame.K_RIGHT:
                        if not self.__game.movepiecewithfocus(None, mutants.Constants.Constants.RIGHT):
                            print("Cannot move that piece to the right.")

            for row in range(self.__board.height):
                for col in range(self.__board.width):
                    #print("Row is " + str(row) + ", col is " + str(col))
                    sq = self.__board.getSquare(col, row)
                    toshow = sq.showing
                    img = self.__images[toshow.name]
                    sidesize = mutants.Constants.Constants.IMAGESIDESIZE
                    x = col * sidesize
                    y = row * sidesize
                    self.__screen.blit(img, (x, y))
                    if (sq.isOccupied()):
                        occupant = sq.piece
                        if issubclass(type(occupant), mutants.PlayerPiece.PlayerPiece):
                            if occupant.canmove() and not occupant.hasattacked:
                                boxcolor = (255, 255, 0)
                            elif occupant.canmove():
                                # indicate to the player that the piece can still move
                                boxcolor = (0, 255, 0)
                            elif not occupant.hasattacked:
                                # indicate to the player that the piece can still attack
                                boxcolor = (255, 0, 0)
                            if occupant.canmove() or not occupant.hasattacked:
                                pygame.draw.rect(self.__screen, boxcolor, (x, y, sidesize, sidesize), 3)

            if drawwhiterect:
                x, y = pygame.mouse.get_pos()
                sidesize = mutants.Constants.Constants.IMAGESIDESIZE
                pygame.draw.rect(self.__screen, (255, 255, 255), (x, y, sidesize, sidesize), 2)

            pygame.display.update()
            if i % 40 == 39:
                if self.__game.mutantturn:
                    self.__game.movemutants()
                    self.__game.mutantturn = False
            self.__game.clearoutdead()
            if self.__game.wavecomplete():
                self.__game.nextwave()

            i += 1

    def runLoopTest(self):
       img1 = pygame.image.load(r"C:\Users\Fitz\Pictures\mut1.png")
       self.__screen.fill((127, 127, 127))
       while (1):
            self.__clock.tick(40)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()

            self.__screen.blit(self.__images["Door"], (0, 0))
            self.__screen.blit(self.__images["Wall"], (40, 40))
            self.__screen.blit(self.__images["Space"], (80, 80))

            x, y = pygame.mouse.get_pos()
            self.__screen.blit(img1, (x, y))
            pygame.display.update()

if __name__ == "__main__":
    import doctest
    doctest.testmod()




