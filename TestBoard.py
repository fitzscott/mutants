import unittest
import Board
import Constants

class TestBoard(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.__board = Board.Board()
        self.__board.width = 10
        self.__board.height = 5
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
        sqN = sq.getNeighbor(Constants.Constants.UP)
        self.assertNotEqual(sqN, None)
        sqN = sq.getNeighbor(Constants.Constants.DOWN)
        self.assertNotEqual(sqN, None)
        sqN = sq.getNeighbor(Constants.Constants.LEFT)
        self.assertNotEqual(sqN, None)
        # We're at the right side of the board, so should not have a neighbor to the right
        sqN = sq.getNeighbor(Constants.Constants.RIGHT)
        self.assertEqual(sqN, None)

    def testNeighborPositions(self):
        sq = self.__board.getSquare(8, 2)
        sqN = sq.getNeighbor(Constants.Constants.UP)
        self.assertEqual(sqN.getYpos(), 1)
        sqN = sq.getNeighbor(Constants.Constants.DOWN)
        self.assertEqual(sqN.getYpos(), 3)
        sqN = sq.getNeighbor(Constants.Constants.LEFT)
        self.assertEqual(sqN.getXpos(), 7)
        sqN = sq.getNeighbor(Constants.Constants.RIGHT)
        self.assertEqual(sqN.getXpos(), 9)

    def testBelowBoard(self):
        sq = self.__board.getSquare(7, 7)
        self.assertEqual(sq, None)


