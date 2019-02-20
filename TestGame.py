__author__ = 'Fitz'

import unittest
import random

import Game as g1
import Human as hum
import Constants as const
import Robot as rob
import Professor as prof

class TestGame(unittest.TestCase):
    def setUp(self):
        pass

    def testG1(self):
        g = g1.Game()
        g.board.getmutants(1)
        g.board.placemutants()
        g.play()
        #try:
        #    g.play()
        #except:
        #    print("Got the usual SystemExit error")

    def testG6(self):
        g = g1.Game("testboard6")
        g.board.getmutants(1)
        g.board.placemutants()
        g.play()
        #try:
        #    g.play()
        #except:
        #    print("Got the usual SystemExit error")

    def testG7(self):
        g = g1.Game("testboard7")
        g.board.getmutants(1)
        # skip placing the mutants - they're defined on the board
        g.play()

    def testG8(self):
        g = g1.Game("testboard8")
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
        g = g1.Game()
        g.board.getmutants(1)
        g.board.placemutants()
        g.play(4000)
        g.nextwave()
        g.play(4000)
        g.nextwave()
        g.play(4000)

    def testGY(self):
        g = g1.Game("testboard9")
        g.board.getmutants(1)
        g.board.placemutants()
        g.play(5000)
        g.nextwave()
        g.play(5000)
        g.nextwave()
        g.play(5000)

    def test1Human(self):
        g = g1.Game("testboard9")
        g.board.getmutants(1)
        g.board.placemutants()
        buck = hum.Human("Buck")
        g.board.placehuman(buck)
        g.play(5000)

    def testManyHumans(self):
        g = g1.Game("testboard9")
        g.board.getmutants(1)
        g.board.placemutants()
        buck = hum.Human("Buck")
        g.board.placehuman(buck)
        molly = hum.Human("Molly")
        g.board.placehuman(molly)
        charlie = hum.Human("Charlie")
        g.board.placehuman(charlie)
        g.play(5000)

    def testHumansAndRobots(self):
        g = g1.Game("testboard9")
        g.board.getmutants(1)
        g.board.placemutants()
        buck = hum.Human("Buck")
        g.board.placehuman(buck)
        molly = hum.Human("Molly")
        g.board.placehuman(molly)
        charlie = hum.Human("Charlie")
        g.board.placehuman(charlie)
        for i in range(const.Constants.NUMROBOTS):
            g.board.placerobot(rob.Robot())
        g.play(500000)

    def testBadMove(self):
        g = g1.Game("testboardA")
        g.board.getmutants(1, 2)
        g.board.placemutants()
        for i in range(3):
            g.board.placerobot(rob.Robot())
        g.play(500000)

    def testNewDist(self):
        g = g1.Game("testboardA")
        g.board.getmutants(1, 2)
        g.board.placemutants()
        charlie = hum.Human("Charlie")
        g.board.placehuman(charlie)
        g.play(500000)

    def testMutantDirectionsAgain(self):
        g = g1.Game("testboardA")
        g.board.getmutants(1, 2)
        g.board.placemutants()
        g.play(500000)

    def testMutantDirectionsYetAgain(self):
        g = g1.Game("testboard5")
        g.board.getmutants(1)
        g.board.placemutants()
        buck = hum.Human("Buck")
        g.board.placehuman(buck)
        molly = hum.Human("Molly")
        g.board.placehuman(molly)
        charlie = hum.Human("Charlie")
        g.board.placehuman(charlie)
        for i in range(const.Constants.NUMROBOTS):
            g.board.placerobot(rob.Robot())
        g.play(500000)

    def testProfessor(self):
        g = g1.Game("testboard5")
        g.board.getmutants(1)
        g.board.placemutants()
        buck = hum.Human("Buck")
        g.board.placehuman(buck)
        molly = hum.Human("Molly")
        g.board.placehuman(molly)
        charlie = hum.Human("Charlie")
        g.board.placehuman(charlie)
        prof1 = prof.Professor()
        g.board.placehuman(prof1)
        for i in range(const.Constants.NUMROBOTS):
            g.board.placerobot(rob.Robot())
        g.play(500000)

    def testRadioactive(self):
        g = g1.Game("testboard5")
        g.board.getmutants(1, 10)
        g.board.placemutants()
        buck = hum.Human("Buck")
        g.board.placehuman(buck)
        molly = hum.Human("Molly")
        g.board.placehuman(molly)
        charlie = hum.Human("Charlie")
        g.board.placehuman(charlie)
        g.play(500000)

    def testComputer(self):
        g = g1.Game("testboardB")
        g.board.getmutants(1)
        g.board.placemutants()
        buck = hum.Human("Buck")
        g.board.placehuman(buck)
        molly = hum.Human("Molly")
        g.board.placehuman(molly)
        charlie = hum.Human("Charlie")
        g.board.placehuman(charlie)
        for i in range(const.Constants.NUMROBOTS):
            g.board.placerobot(rob.Robot())
        g.play(500000)

    def testBoardB(self):
        g = g1.Game("testboardB")
        g.board.getmutants(1)
        g.board.placemutants()
        buck = hum.Human("Buck")
        g.board.placehuman(buck)
        molly = hum.Human("Molly")
        g.board.placehuman(molly)
        charlie = hum.Human("Charlie")
        g.board.placehuman(charlie)
        prof1 = prof.Professor()
        g.board.placehuman(prof1)
        for i in range(const.Constants.NUMROBOTS):
            g.board.placerobot(rob.Robot())
        g.play(500000)

    def testBoardC(self):
        g = g1.Game("testboardC")
        g.board.getmutants(1)
        g.board.placemutants()
        buck = hum.Human("Buck")
        g.board.placehuman(buck)
        molly = hum.Human("Molly")
        g.board.placehuman(molly)
        charlie = hum.Human("Charlie")
        g.board.placehuman(charlie)
        prof1 = prof.Professor()
        g.board.placehuman(prof1)
        for i in range(const.Constants.NUMROBOTS):
            g.board.placerobot(rob.Robot())
        g.play(500000)

    def testHyper(self):
        g = g1.Game("testboardC")
        g.board.getmutants(1)
        g.board.placemutants()
        g.board.hyperthreshhold = 57        # yow
        buck = hum.Human("Buck")
        g.board.placehuman(buck)
        molly = hum.Human("Molly")
        g.board.placehuman(molly)
        charlie = hum.Human("Charlie")
        g.board.placehuman(charlie)
        prof1 = prof.Professor()
        g.board.placehuman(prof1)
        for i in range(const.Constants.NUMROBOTS):
            g.board.placerobot(rob.Robot())
        g.play(500000)

    def testBoardD(self):
        g = g1.Game("testboardD")
        g.board.getmutants(1)
        g.board.placemutants()
        buck = hum.Human("Buck")
        g.board.placehuman(buck)
        molly = hum.Human("Molly")
        g.board.placehuman(molly)
        charlie = hum.Human("Charlie")
        g.board.placehuman(charlie)
        prof1 = prof.Professor()
        g.board.placehuman(prof1)
        for i in range(const.Constants.NUMROBOTS):
            g.board.placerobot(rob.Robot())
        g.play(500000)

    def testBoardD2(self):
        g = g1.Game("testboardD")
        g.board.getmutants(1)
        g.board.placemutants()
        buck = hum.Human("Buck")
        g.board.placehuman(buck)
        molly = hum.Human("Molly")
        g.board.placehuman(molly)
        charlie = hum.Human("Charlie")
        g.board.placehuman(charlie)
        jeb = hum.Human("Jeb")
        g.board.placehuman(jeb)
        prof1 = prof.Professor()
        g.board.placehuman(prof1)
        for i in range(const.Constants.NUMROBOTS):
            g.board.placerobot(rob.Robot())
        g.play(500000)

    def testBoardE(self):
        g = g1.Game("testboardE")
        g.board.getmutants(1)
        g.board.placemutants()
        buck = hum.Human("Buck")
        g.board.placehuman(buck)
        molly = hum.Human("Molly")
        g.board.placehuman(molly)
        charlie = hum.Human("Charlie")
        g.board.placehuman(charlie)
        jeb = hum.Human("Jeb")
        g.board.placehuman(jeb)
        prof1 = prof.Professor()
        g.board.placehuman(prof1)
        for i in range(const.Constants.NUMROBOTS):
            g.board.placerobot(rob.Robot())
        g.play(500000)

    def testBoardF(self):
        g = g1.Game("testboardF")
        g.board.getmutants(1)
        g.board.placemutants()
        buck = hum.Human("Buck")
        g.board.placehuman(buck)
        molly = hum.Human("Molly")
        g.board.placehuman(molly)
        charlie = hum.Human("Charlie")
        g.board.placehuman(charlie)
        jeb = hum.Human("Jeb")
        g.board.placehuman(jeb)
        prof1 = prof.Professor()
        g.board.placehuman(prof1)
        for i in range(const.Constants.NUMROBOTS):
            g.board.placerobot(rob.Robot())
        g.play(500000)

    def testDeadComputer(self):
        g = g1.Game("testboard2")
        g.board.getmutants(1)
        g.board.placemutants()
        g.play()

    def testBoard6(self):
        g = g1.Game("Board6")
        g.board.getmutants(1)
        g.board.placemutants()
        buck = hum.Human("Buck")
        g.board.placehuman(buck)
        molly = hum.Human("Molly")
        g.board.placehuman(molly)
        charlie = hum.Human("Charlie")
        g.board.placehuman(charlie)
        jeb = hum.Human("Jeb")
        g.board.placehuman(jeb)
        prof1 = prof.Professor()
        g.board.placehuman(prof1)
        for i in range(const.Constants.NUMROBOTS):
            g.board.placerobot(rob.Robot())
        g.play(500000)

