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

    def testBoard2(self):
        self.__display.loadResources("testboard2")
        self.__display.runLoop()