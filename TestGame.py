__author__ = 'Fitz'

import unittest
import random

import mutants.Game
import mutants.Human
import mutants.Constants
import mutants.Robot
import mutants.Professor

class TestGame(unittest.TestCase):
    def setUp(self):
        pass

    def testG1(self):
        g = mutants.Game.Game()
        g.board.getmutants(1)
        g.board.placemutants()
        g.play()
        #try:
        #    g.play()
        #except:
        #    print("Got the usual SystemExit error")

    def testG6(self):
        g = mutants.Game.Game("testboard6")
        g.board.getmutants(1)
        g.board.placemutants()
        g.play()
        #try:
        #    g.play()
        #except:
        #    print("Got the usual SystemExit error")

    def testG7(self):
        g = mutants.Game.Game("testboard7")
        g.board.getmutants(1)
        # skip placing the mutants - they're defined on the board
        g.play()

    def testG8(self):
        g = mutants.Game.Game("testboard8")
        g.board.getmutants(1)
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
        g.board.getmutants(1)
        g.board.placemutants()
        g.play(4000)
        g.nextwave()
        g.play(4000)
        g.nextwave()
        g.play(4000)

    def testGY(self):
        g = mutants.Game.Game("testboard9")
        g.board.getmutants(1)
        g.board.placemutants()
        g.play(5000)
        g.nextwave()
        g.play(5000)
        g.nextwave()
        g.play(5000)

    def test1Human(self):
        g = mutants.Game.Game("testboard9")
        g.board.getmutants(1)
        g.board.placemutants()
        bart = mutants.Human.Human("Bart")
        g.board.placehuman(bart)
        g.play(5000)

    def testManyHumans(self):
        g = mutants.Game.Game("testboard9")
        g.board.getmutants(1)
        g.board.placemutants()
        bart = mutants.Human.Human("Bart")
        g.board.placehuman(bart)
        molly = mutants.Human.Human("Molly")
        g.board.placehuman(molly)
        charlie = mutants.Human.Human("Charlie")
        g.board.placehuman(charlie)
        g.play(5000)

    def testHumansAndRobots(self):
        g = mutants.Game.Game("testboard9")
        g.board.getmutants(1)
        g.board.placemutants()
        bart = mutants.Human.Human("Bart")
        g.board.placehuman(bart)
        molly = mutants.Human.Human("Molly")
        g.board.placehuman(molly)
        charlie = mutants.Human.Human("Charlie")
        g.board.placehuman(charlie)
        for i in range(mutants.Constants.Constants.NUMROBOTS):
            g.board.placerobot(mutants.Robot.Robot())
        g.play(500000)

    def testBadMove(self):
        g = mutants.Game.Game("testboardA")
        g.board.getmutants(1, 2)
        g.board.placemutants()
        for i in range(3):
            g.board.placerobot(mutants.Robot.Robot())
        g.play(500000)

    def testNewDist(self):
        g = mutants.Game.Game("testboardA")
        g.board.getmutants(1, 2)
        g.board.placemutants()
        charlie = mutants.Human.Human("Charlie")
        g.board.placehuman(charlie)
        g.play(500000)

    def testMutantDirectionsAgain(self):
        g = mutants.Game.Game("testboardA")
        g.board.getmutants(1, 2)
        g.board.placemutants()
        g.play(500000)

    def testMutantDirectionsYetAgain(self):
        g = mutants.Game.Game("testboard5")
        g.board.getmutants(1)
        g.board.placemutants()
        bart = mutants.Human.Human("Bart")
        g.board.placehuman(bart)
        molly = mutants.Human.Human("Molly")
        g.board.placehuman(molly)
        charlie = mutants.Human.Human("Charlie")
        g.board.placehuman(charlie)
        for i in range(mutants.Constants.Constants.NUMROBOTS):
            g.board.placerobot(mutants.Robot.Robot())
        g.play(500000)

    def testProfessor(self):
        g = mutants.Game.Game("testboard5")
        g.board.getmutants(1)
        g.board.placemutants()
        bart = mutants.Human.Human("Bart")
        g.board.placehuman(bart)
        molly = mutants.Human.Human("Molly")
        g.board.placehuman(molly)
        charlie = mutants.Human.Human("Charlie")
        g.board.placehuman(charlie)
        prof = mutants.Professor.Professor()
        g.board.placehuman(prof)
        for i in range(mutants.Constants.Constants.NUMROBOTS):
            g.board.placerobot(mutants.Robot.Robot())
        g.play(500000)

    def testRadioactive(self):
        g = mutants.Game.Game("testboard5")
        g.board.getmutants(1, 10)
        g.board.placemutants()
        bart = mutants.Human.Human("Bart")
        g.board.placehuman(bart)
        molly = mutants.Human.Human("Molly")
        g.board.placehuman(molly)
        charlie = mutants.Human.Human("Charlie")
        g.board.placehuman(charlie)
        g.play(500000)

    def testComputer(self):
        g = mutants.Game.Game("testboardB")
        g.board.getmutants(1)
        g.board.placemutants()
        bart = mutants.Human.Human("Bart")
        g.board.placehuman(bart)
        molly = mutants.Human.Human("Molly")
        g.board.placehuman(molly)
        charlie = mutants.Human.Human("Charlie")
        g.board.placehuman(charlie)
        for i in range(mutants.Constants.Constants.NUMROBOTS):
            g.board.placerobot(mutants.Robot.Robot())
        g.play(500000)

    def testBoardB(self):
        g = mutants.Game.Game("testboardB")
        g.board.getmutants(1)
        g.board.placemutants()
        bart = mutants.Human.Human("Bart")
        g.board.placehuman(bart)
        molly = mutants.Human.Human("Molly")
        g.board.placehuman(molly)
        charlie = mutants.Human.Human("Charlie")
        g.board.placehuman(charlie)
        prof = mutants.Professor.Professor()
        g.board.placehuman(prof)
        for i in range(mutants.Constants.Constants.NUMROBOTS):
            g.board.placerobot(mutants.Robot.Robot())
        g.play(500000)

    def testBoardC(self):
        g = mutants.Game.Game("testboardC")
        g.board.getmutants(1)
        g.board.placemutants()
        bart = mutants.Human.Human("Bart")
        g.board.placehuman(bart)
        molly = mutants.Human.Human("Molly")
        g.board.placehuman(molly)
        charlie = mutants.Human.Human("Charlie")
        g.board.placehuman(charlie)
        prof = mutants.Professor.Professor()
        g.board.placehuman(prof)
        for i in range(mutants.Constants.Constants.NUMROBOTS):
            g.board.placerobot(mutants.Robot.Robot())
        g.play(500000)

    def testHyper(self):
        g = mutants.Game.Game("testboardC")
        g.board.getmutants(1)
        g.board.placemutants()
        g.board.hyperthreshhold = 57        # yow
        bart = mutants.Human.Human("Bart")
        g.board.placehuman(bart)
        molly = mutants.Human.Human("Molly")
        g.board.placehuman(molly)
        charlie = mutants.Human.Human("Charlie")
        g.board.placehuman(charlie)
        prof = mutants.Professor.Professor()
        g.board.placehuman(prof)
        for i in range(mutants.Constants.Constants.NUMROBOTS):
            g.board.placerobot(mutants.Robot.Robot())
        g.play(500000)

    def testBoardD(self):
        g = mutants.Game.Game("testboardD")
        g.board.getmutants(1)
        g.board.placemutants()
        bart = mutants.Human.Human("Bart")
        g.board.placehuman(bart)
        molly = mutants.Human.Human("Molly")
        g.board.placehuman(molly)
        charlie = mutants.Human.Human("Charlie")
        g.board.placehuman(charlie)
        prof = mutants.Professor.Professor()
        g.board.placehuman(prof)
        for i in range(mutants.Constants.Constants.NUMROBOTS):
            g.board.placerobot(mutants.Robot.Robot())
        g.play(500000)

