import unittest
import mutants.Board
import mutants.Constants

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.__board = mutants.Board.Board()
        self.__board.setWidth(10)
        self.__board.setHeight(5)
        self.__board.fill()

    def tearDown(self):
        pass

    def testGetSquare(self):
        sq = self.__board.getSquare(9, 2)
        print("Position of square: X = " + str(sq.getXpos()) + ", Y = " +
              str(sq.getYpos()))
        self.assertEqual(sq.getXpos(), 9)
        self.assertEqual(sq.getYpos(), 2)

    def testGetNeighbors(self):
        sq = self.__board.getSquare(9, 2)
        sqN = sq.getNeighbor(mutants.Constants.Constants.UP)
        self.assertNotEqual(sqN, None)
        sqN = sq.getNeighbor(mutants.Constants.Constants.DOWN)
        self.assertNotEqual(sqN, None)
        sqN = sq.getNeighbor(mutants.Constants.Constants.LEFT)
        self.assertNotEqual(sqN, None)
        # We're at the right side of the board, so should not have a neighbor to the right
        sqN = sq.getNeighbor(mutants.Constants.Constants.RIGHT)
        self.assertEqual(sqN, None)

    def testNeighborPositions(self):
        sq = self.__board.getSquare(8, 2)
        sqN = sq.getNeighbor(mutants.Constants.Constants.UP)
        self.assertEqual(sqN.getYpos(), 1)
        sqN = sq.getNeighbor(mutants.Constants.Constants.DOWN)
        self.assertEqual(sqN.getYpos(), 3)
        sqN = sq.getNeighbor(mutants.Constants.Constants.LEFT)
        self.assertEqual(sqN.getXpos(), 7)
        sqN = sq.getNeighbor(mutants.Constants.Constants.RIGHT)
        self.assertEqual(sqN.getXpos(), 9)


