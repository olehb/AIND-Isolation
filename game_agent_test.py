import unittest
from isolation import Board
from game_agent import AlphaBetaPlayer


class TestGameBoard(unittest.TestCase):
    def setUp(self):
        state = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 41, 68]
        player_1 = AlphaBetaPlayer()
        player_2 = AlphaBetaPlayer()
        self.game = Board(player_1, player_2, raw_state=state)

    def _test_alphabeta(self):
        self.game.play()
    
    def test_rotate(self):
        self.assertEqual(self.game.rotate().rotate().rotate().rotate().hash(), self.game.hash())

    def test_diag_reflect(self):
        self.assertEqual(self.game.diag_reflect().diag_reflect().hash(), self.game.hash())

    def test_mutations(self):
        self.assertEqual(len(list(self.game.mutations())), 6)
        # for board in self.game.mutations():
        #     print(board.to_string())

if __name__ == '__main__':
    unittest.main()
