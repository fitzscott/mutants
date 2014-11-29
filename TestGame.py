__author__ = 'Fitz'

import unittest
import random

import mutants.Game
import mutants.Human
import mutants.Constants
import mutants.Robot

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

    def testGY(self):
        g = mutants.Game.Game("testboard9")
        g.getmutants()
        g.placemutants()
        g.play(5000)
        g.nextwave()
        g.play(5000)
        g.nextwave()
        g.play(5000)

    def test1Human(self):
        g = mutants.Game.Game("testboard9")
        g.getmutants()
        g.placemutants()
        bart = mutants.Human.Human("Bart")
        g.placehuman(bart)
        g.play(5000)

    def testManyHumans(self):
        g = mutants.Game.Game("testboard9")
        g.getmutants()
        g.placemutants()
        bart = mutants.Human.Human("Bart")
        g.placehuman(bart)
        molly = mutants.Human.Human("Molly")
        g.placehuman(molly)
        charlie = mutants.Human.Human("Charlie")
        g.placehuman(charlie)
        g.play(5000)

    def testHumansAndRobots(self):
        g = mutants.Game.Game("testboard9")
        g.getmutants()
        g.placemutants()
        bart = mutants.Human.Human("Bart")
        g.placehuman(bart)
        molly = mutants.Human.Human("Molly")
        g.placehuman(molly)
        charlie = mutants.Human.Human("Charlie")
        g.placehuman(charlie)
        for i in range(mutants.Constants.Constants.NUMROBOTS):
            g.placerobot(mutants.Robot.Robot())
        g.play(500000)

    def testBadMove(self):
        g = mutants.Game.Game("testboardA")
        g.getmutants(2)
        g.placemutants()
        for i in range(3):
            g.placerobot(mutants.Robot.Robot())
        g.play(500000)

    def testNewDist(self):
        g = mutants.Game.Game("testboardA")
        g.getmutants(2)
        g.placemutants()
        charlie = mutants.Human.Human("Charlie")
        g.placehuman(charlie)
        g.play(500000)

    def testMutantDirectionsAgain(self):
        g = mutants.Game.Game("testboardA")
        g.getmutants(2)
        g.placemutants()
        g.play(500000)

    def testMutantDirectionsYetAgain(self):
        g = mutants.Game.Game("testboard5")
        g.getmutants()
        g.placemutants()
        bart = mutants.Human.Human("Bart")
        g.placehuman(bart)
        molly = mutants.Human.Human("Molly")
        g.placehuman(molly)
        charlie = mutants.Human.Human("Charlie")
        g.placehuman(charlie)
        for i in range(mutants.Constants.Constants.NUMROBOTS):
            g.placerobot(mutants.Robot.Robot())
        g.play(500000)
