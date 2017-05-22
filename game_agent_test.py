import unittest
from isolation import Board
from game_agent import AlphaBetaPlayer


class TestGameBoard(unittest.TestCase):
    def setUp(self):
        state = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 41, 68]
        player_1 = AlphaBetaPlayer()
        player_2 = AlphaBetaPlayer()
        self.game = Board(player_1, player_2, raw_state=state)

    def test_alphabeta(self):
        self.game.play()


if __name__ == '__main__':
    unittest.main()
