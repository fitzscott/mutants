import unittest
import mutants.BoardFile
import mutants.Constants

class TestBoardFile(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.__bf = mutants.BoardFile.BoardFile()

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


