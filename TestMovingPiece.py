import unittest
import mutants.MovingPiece
import mutants.Board
import mutants.Constants

class TestMovingPiece(unittest.TestCase):
    def setUp(self):
        self.__board = mutants.Board.Board()
        self.__board.width = 10
        self.__board.height = 5
        self.__board.fill()

    def tearDown(self):
        pass

    def testCreateMovingPiece(self):
        sq = self.__board.getSquare(1, 2)
        mp = mutants.MovingPiece.MovingPiece("Speedy", None, 5)
        mp.setPosition(sq)
        self.assertEqual(mp.getPosition().getXpos(), 1)
        self.assertNotEqual(mp.getPosition().getYpos(), 1)

    def testMoveMovingPiece(self):
        sq = self.__board.getSquare(9, 2)
        mp = mutants.MovingPiece.MovingPiece("Dopey", None, 3)
        mp.setPosition(sq)
        self.assertEqual(mp.getPosition().getXpos(), 9)
        self.assertEqual(mp.getPosition().getYpos(), 2)
        self.assertEqual(mp.getRemainingMovement(), 3)
        mp.moveindirection(mutants.Constants.Constants.LEFT)
        self.assertEqual(mp.getPosition().getXpos(), 8)
        self.assertEqual(mp.getPosition().getYpos(), 2)
        self.assertEqual(mp.getRemainingMovement(), 2)
        self.assertFalse(sq.isOccupied())
        mp.moveindirection(mutants.Constants.Constants.UP)
        self.assertEqual(mp.getPosition().getXpos(), 8)
        self.assertEqual(mp.getPosition().getYpos(), 1)
        self.assertEqual(mp.getRemainingMovement(), 1)
        mp.resetMovement()
        self.assertEqual(mp.getRemainingMovement(), 3)
        self.assertTrue(mp.moveindirection(mutants.Constants.Constants.DOWN))
        self.assertTrue(mp.moveindirection(mutants.Constants.Constants.DOWN))
        self.assertTrue(mp.moveindirection(mutants.Constants.Constants.DOWN))
        self.assertEqual(mp.getRemainingMovement(), 0)
        self.assertFalse(mp.moveindirection(mutants.Constants.Constants.LEFT))


