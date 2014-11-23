__author__ = 'Fitz'

import unittest
import random

import mutants.Game

class TestGame(unittest.TestCase):
    def setUp(self):
        pass

    def testG1(self):
        g = mutants.Game.Game()
        g.getmutants()
        g.placemutants()
        g.play()
        #try:
        #    g.play()
        #except:
        #    print("Got the usual SystemExit error")

    def testG6(self):
        g = mutants.Game.Game("testboard6")
        g.getmutants()
        g.placemutants()
        g.play()
        #try:
        #    g.play()
        #except:
        #    print("Got the usual SystemExit error")

    def testG7(self):
        g = mutants.Game.Game("testboard7")
        g.getmutants()
        # skip placing the mutants - they're defined on the board
        g.play()

    def testG8(self):
        g = mutants.Game.Game("testboard8")
        g.getmutants()
        # skip placing the mutants - they're defined on the board
        g.play()

    def testRand(self):
        # not really a test of the game - testing the randomizer
        # Ah - confused random's randint with NumPy's.  :(
        max = 10
        for i in range(1000):
            #x = random.randint(0, max)
            x = random.randint(max)
            print("Random is " + str(x))
            self.assertTrue(x < max)

    def testGX(self):
        g = mutants.Game.Game()
        g.getmutants()
        g.placemutants()
        g.play(4000)
        g.nextwave()
        g.play(4000)
        g.nextwave()
        g.play(4000)

