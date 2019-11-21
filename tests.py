import unittest
from XOX import TicTacToe


class TestTicTacToe(unittest.TestCase):
    def setUp(self):
        self.game = TicTacToe()

    def test_situationCheck(self):
        self.game.field = ['X', 'X', 'X', ' ', 'O', ' ', 'O', ' ', 'O']
        self.assertEqual(self.game.situationCheck(), 0)
        self.game.field = ['X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X']
        self.assertEqual(self.game.situationCheck(), 0)
        self.game.field = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        self.assertEqual(self.game.situationCheck(), 1)


if __name__ == '__main__':
    unittest.main()
