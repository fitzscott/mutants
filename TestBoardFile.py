import unittest
import BoardFile
import Constants
import Mutant

class TestBoardFile(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.__bf = BoardFile.BoardFile()

    def tearDown(self):
        pass

    def testOpenFile(self):
        self.__bf.readFromFile("testboard1")

    def testLineAndColCount(self):
        self.__bf.readFromFile("testboard1")
        self.assertEqual(self.__bf.columns, 30)
        self.assertEqual(self.__bf.lines, 9)

    def testCreateBoard(self):
        self.__bf.readFromFile("testboard1")
        b = self.__bf.createBoard()
        self.assertEqual(b.getSquare(0, 0).getTerrain().name, "Wall")
        self.assertEqual(b.getSquare(1, 1).getTerrain().name, "Space")
        self.assertEqual(b.getSquare(0, 4).getTerrain().name, "Door")
        self.assertNotEqual(b.getSquare(29, 5).getTerrain().name, "Space")
        self.assertNotEqual(b.getSquare(0, 8).getTerrain().name, "Space")

    def testAnotherBoard(self):
        self.__bf.readFromFile("testboard3")
        b = self.__bf.createBoard()

    def testYetAnotherBoard(self):
        self.__bf.readFromFile("testboard4")
        b = self.__bf.createBoard()

    def testAgainAnotherBoard(self):
        self.__bf.readFromFile("testboard5")
        b = self.__bf.createBoard()

    def look(self, sq, direction, distance):
        sqdir = sq.getNeighbor(direction, distance)
        #print("Seeing " + sqdir.showing.name + " (class " + str(type(sqdir.showing)) + \
        #      ") in direction " + str(direction))
        return(sqdir)

    def doneLooking(self, sq):
        return(sq.showing.name != "Wall" and sq.showing.name != "Door")

    def lookAround(self, sq):
        distance = 1
        things2find = True
        thingsseen = [-1, -1, -1, -1]   # up, down, left, right
        up = True
        down = True
        left = True
        right = True
        while things2find:
            if up:
                nsq = self.look(sq, Constants.Constants.UP, distance)
                if type(nsq.showing) in Mutant.Mutant.MUTANTINTEREST:
                    idx = Mutant.Mutant.MUTANTINTEREST.index(type(nsq.showing))
                    if idx > thingsseen[0]:
                        thingsseen[0] = idx
                up = self.doneLooking(nsq)
            if down:
                nsq = self.look(sq, Constants.Constants.DOWN, distance)
                if type(nsq.showing) in Mutant.Mutant.MUTANTINTEREST:
                    idx = Mutant.Mutant.MUTANTINTEREST.index(type(nsq.showing))
                    if idx > thingsseen[1]:
                        thingsseen[1] = idx
                down = self.doneLooking(nsq)
            if left:
                nsq = self.look(sq, Constants.Constants.LEFT, distance)
                if type(nsq.showing) in Mutant.Mutant.MUTANTINTEREST:
                    idx = Mutant.Mutant.MUTANTINTEREST.index(type(nsq.showing))
                    if idx > thingsseen[2]:
                        thingsseen[2] = idx
                left = self.doneLooking(nsq)
            if right:
                nsq = self.look(sq, Constants.Constants.RIGHT, distance)
                if type(nsq.showing) in Mutant.Mutant.MUTANTINTEREST:
                    idx = Mutant.Mutant.MUTANTINTEREST.index(type(nsq.showing))
                    if idx > thingsseen[3]:
                        thingsseen[3] = idx
                right = self.doneLooking(nsq)
            distance += 1
            things2find = up or down or left or right
        #print("Up: " + str(Mutant.Mutant.MUTANTINTEREST[thingsseen[0]]))
        #print("Down: " + str(Mutant.Mutant.MUTANTINTEREST[thingsseen[1]]))
        #print("Left: " + str(Mutant.Mutant.MUTANTINTEREST[thingsseen[2]]))
        #print("Right: " + str(Mutant.Mutant.MUTANTINTEREST[thingsseen[3]]))
        max = maxidx = -1
        for i in range(len(thingsseen)):
            if thingsseen[i] > max:
                max = thingsseen[i]
                maxidx = i
        return (maxidx)     # direction to go

    def testNeighbors(self):
        self.__bf.readFromFile("testboard5")
        b = self.__bf.createBoard()
        m = Mutant.Mutant()
        sq = b.getSquare(27, 12)
        self.assertEqual(sq.getTerrain().name, "Space")
        sq.addPiece(m)
        self.assertEqual(sq.showing.name, "Mutant")
        dir = self.lookAround(sq)
        self.assertEqual(dir, 0)
        sq = b.getSquare(28, 9)
        dir = self.lookAround(sq)
        self.assertEqual(dir, 1)
        sq = b.getSquare(13, 2)
        dir = self.lookAround(sq)
        self.assertEqual(dir, 1)
        sq = b.getSquare(12, 12)
        dir = self.lookAround(sq)
        self.assertEqual(dir, 0)

    def testNeighbors2(self):
        self.__bf.readFromFile("testboard5")
        b = self.__bf.createBoard()
        m = Mutant.Mutant()
        sq = b.getSquare(27, 12)
        self.assertEqual(sq.getTerrain().name, "Space")
        self.assertTrue(m.setPosition(sq))
        self.assertEqual(sq.showing.name, "Mutant")
        dir = m.chooseDirection()
        self.assertEqual(dir, 0)
        sq = b.getSquare(28, 9)
        self.assertTrue(m.setPosition(sq))
        dir = m.chooseDirection()
        self.assertEqual(dir, 1)
        sq = b.getSquare(13, 2)
        self.assertTrue(m.setPosition(sq))
        dir = m.chooseDirection()
        self.assertEqual(dir, 1)
        sq = b.getSquare(12, 12)
        self.assertTrue(m.setPosition(sq))
        dir = m.chooseDirection()
        self.assertEqual(dir, 0)

    def testYetAgainAnotherBoard(self):
        """
        try out the "courtyard" board
        """
        self.__bf.readFromFile("testboard6")
        b = self.__bf.createBoard()


