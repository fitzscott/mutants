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
        pygame.init()
        pygame.mixer.init()
        self.__screen = pygame.display.set_mode(mutants.Constants.Constants.WINSIZE, pygame.DOUBLEBUF)
        pygame.display.set_caption("Attack of the Mutants!")
        self.__clock = pygame.time.Clock()
        #pygame.mouse.set_visible(0)
        self.__images = {}
        self.__board = None
        self.__game = game
        self.__bgcolor = (223, 223, 223)

    def loadBoard(self, flnm):
        bf = mutants.BoardFile.BoardFile()
        bf.readFromFile(flnm)
        self.__board = bf.createBoard()
        self.__board.addmessage("The mutants are attacking!")

    def loadImage(self, cwd, typestr):
        flnm = os.path.join(cwd, "Resources", "Images", typestr + ".png")
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
        self.loadImage(cwd, "Chainsaw")
        self.loadImage(cwd, "SpareParts")
        self.loadImage(cwd, "Molly")
        self.loadImage(cwd, "Buck")
        self.loadImage(cwd, "Charlie")
        self.loadImage(cwd, "Jeb")
        self.loadImage(cwd, "Robot")
        self.loadImage(cwd, "Computer")
        self.loadImage(cwd, "Tombstone")
        self.loadImage(cwd, "Debris")
        for i in range(9):
            self.loadImage(cwd, "Mutant0" + str(i+1))
            self.loadImage(cwd, "LeaderMutant0" + str(i+1))
            self.loadImage(cwd, "RadioactiveMutant0" + str(i+1))
            self.loadImage(cwd, "HyperRadioactiveMutant0" + str(i+1))
        self.loadImage(cwd, "Professor")
        self.loadBoard(boardname)
        self.__font = pygame.font.SysFont("Courier", 12)
        msgdisp = self.__font.render("Attack of the Mutants!", 1, (63, 0, 63), self.__bgcolor)
        self.__messageheight = msgdisp.get_size()[1] + 1
        maxmessages = (mutants.Constants.Constants.WINSIZE[1] - self.bottomofboard()) / self.__messageheight - 1
        self.__board.maxmessages = maxmessages
        buttonfont = pygame.font.SysFont("Courier", 24)
        self.__nextbuttonmsg = buttonfont.render(" Next Turn ", 1, (255, 255, 255), (0, 127, 0))
        self.__nextbuttonsize = self.__nextbuttonmsg.get_size()

    def message(self):
        y = self.bottomofboard() + 1
        msglist = self.__board.messages
        for i in range(len(msglist)):
            msgdisp = self.__font.render(msglist[i], 1, (63, 0, 63), self.__bgcolor)
            self.__screen.blit(msgdisp, (5, y))
            y += self.__messageheight
        self.__screen.blit(self.__nextbuttonmsg, (797 - self.__nextbuttonsize[0], self.bottomofboard() + 3))

    def addmessage(self, msg):
        self.__board.addmessage(msg)

    def drawboard(self, drawwhiterect=False):
        for row in range(self.__board.height):
            for col in range(self.__board.width):
                #print("Row is " + str(row) + ", col is " + str(col))
                sq = self.__board.getSquare(col, row)
                toshow = sq.showing
                if toshow.image in self.__images:
                    img = self.__images[toshow.image]
                else:
                    print("Tried showing " + toshow.name + ", but couldn't.")
                sidesize = mutants.Constants.Constants.IMAGESIDESIZE
                x = col * sidesize
                y = row * sidesize
                self.__screen.blit(img, (x, y))
                if (sq.isOccupied()):
                    occupant = sq.piece
                    if issubclass(type(occupant), mutants.PlayerPiece.PlayerPiece):
                        if occupant.canmove() and not occupant.hasattacked:
                            boxcolor = (255, 0, 255)
                        elif occupant.canmove():
                            # indicate to the player that the piece can still move
                            boxcolor = (0, 0, 255)
                        elif not occupant.hasattacked:
                            # indicate to the player that the piece can still attack
                            boxcolor = (255, 0, 0)
                        if occupant.canmove() or not occupant.hasattacked:
                            pygame.draw.rect(self.__screen, boxcolor, (x, y, sidesize, sidesize), 3)

        if drawwhiterect:
            x, y = pygame.mouse.get_pos()
            sidesize = mutants.Constants.Constants.IMAGESIDESIZE
            halfsize = sidesize // 2
            xp = x - halfsize
            if xp < 0:
                xp = 0
            yp = y - halfsize
            if yp < 0:
                yp = 0
            pygame.draw.rect(self.__screen, (255, 255, 255), (xp, yp, sidesize, sidesize), 2)

    @property
    def board(self):
        return(self.__board)

    def runLoop(self, maxtix=10000000):
        i = 0
        gamecontinues = True
        drawwhiterect = False
        while (i < maxtix):
            self.__clock.tick(40)
            self.__screen.fill(self.__bgcolor)

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
                            #if pygame.mouse.get_pressed()[0]:
                            occupant = sq.piece
                            if event.button == 1:       # left click
                                #print("Left click on " + occupant.fullname)
                                if issubclass(type(occupant), mutants.PlayerPiece.PlayerPiece):
                                    self.__game.clearfoci()
                                    occupant.focus = True
                                    #print(occupant.name + " has focus at (" + str(col) + ", " + str(row) + ").")
                                else:
                                    self.__board.addmessage(occupant.synopsis())
                                    self.__game.clearfoci()
                            #elif pygame.mouse.get_pressed()[2]:    # right-click?
                            elif event.button == 3:     # right click
                                activepiece = self.__game.piecewithfocus()
                                if activepiece != None:
                                    #print("Right click from " + activepiece.fullname + " on " + sq.showing.fullname)
                                    activepiece.attack(sq)
                        elif sq.hasindicator():
                            self.__board.addmessage("That is a " + sq.indicator.name)
                            self.__game.clearfoci()
                        elif sq.hasequipment():
                            self.__board.addmessage("That is a " + sq.getequipment().name)
                            self.__game.clearfoci()
                    else:
                        self.__game.mutantturn = True
                        #gamecontinues = self.__game.nextturn()
                        self.__game.nextturn()

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:       # left click
                        x, y = pygame.mouse.get_pos()
                        col = x // mutants.Constants.Constants.IMAGESIDESIZE
                        row = y // mutants.Constants.Constants.IMAGESIDESIZE
                        sq = self.__board.getSquare(col, row)
                        self.__game.movepiecewithfocus(sq)
                        #if not self.__game.movepiecewithfocus(sq):
                        #    print("Cannot move that piece to (" + str(col) + ", " + str(row) + ").")
                        drawwhiterect = False

                if event.type == pygame.MOUSEMOTION:
                    if pygame.mouse.get_pressed()[0]:
                        drawwhiterect = True

                if event.type == pygame.KEYDOWN:
                    piece = self.__game.piecewithfocus()
                    if piece != None:
                        pickup = not (pygame.key.get_mods() & KMOD_SHIFT)
                        #if pickup:
                        #    print(piece.fullname + " is in pick-up mode")
                        #else:
                        #    print(piece.fullname + " does not want to pick stuff up")
                        piece.wantpickup = pickup
                        if event.key == pygame.K_UP:
                            piece.moveindirection(mutants.Constants.Constants.UP)
                        if event.key == pygame.K_DOWN:
                            piece.moveindirection(mutants.Constants.Constants.DOWN)
                        if event.key == pygame.K_LEFT:
                            piece.moveindirection(mutants.Constants.Constants.LEFT)
                        if event.key == pygame.K_RIGHT:
                            piece.moveindirection(mutants.Constants.Constants.RIGHT)
                        if event.key == pygame.K_s:
                            piece.special()
                        if event.key == pygame.K_h:
                            piece.healthyself()
                    else:
                        if event.key == pygame.K_i:
                            if sq != None and sq.isOccupied():
                                self.__board.addmessage(sq.piece.diagnosis())

            self.drawboard(drawwhiterect)
            self.message()
            pygame.display.update()
            if i % 40 == 39:
                i += 1
                if self.__game.mutantturn:
                    self.__game.mutantturn = False
                    self.__game.board.movemutants()
                    self.__game.board.mutantattack()
                self.__game.clearoutdead()
                if self.__game.wavecomplete():
                    gamecontinues = self.__game.nextwave()

            if gamecontinues:
                i += 1

    def bottomofboard(self):
        return (self.__board.height * mutants.Constants.Constants.IMAGESIDESIZE)

if __name__ == "__main__":
    import doctest
    doctest.testmod()




