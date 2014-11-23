__author__ = 'Fitz'

import unittest
import mutants.Display

class TestDisplay(unittest.TestCase):
    def setUp(self):
        self.__display = mutants.Display.Display()
        #self.__display.loadResources("testboard1")

    #def testEventLoop(self):
    #    self.__display.runLoopTest()

    #def testRealEventLoop(self):
    #    self.__display.runLoop()

    def parmBoard(self, boardname):
        self.__display.loadResources(boardname)
        self.__display.runLoop()

    def testBoard(self):
        self.parmBoard("testboard6")
