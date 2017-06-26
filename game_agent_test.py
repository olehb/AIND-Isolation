import unittest
from isolation import Board
from game_agent import AlphaBetaPlayer, custom_score, custom_score_2, custom_score_3
from game_agent import get_mutation_hashes, take_longest_path


class TestGameBoard(unittest.TestCase):
    def setUp(self):
        state = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 41, 68]
        player_1 = AlphaBetaPlayer(score_fn=custom_score_2)
        player_2 = AlphaBetaPlayer(score_fn=custom_score)
        self.game = Board(player_1, player_2, raw_state=state, p1_name="player 1", p2_name="player 2")

    def test_alphabeta(self):
        print(self.game.play())
    
    def test_rotate(self):
        self.assertEqual(self.game.rotate().rotate().rotate().rotate().hash(), self.game.hash())

    def test_diag_reflect(self):
        self.assertEqual(self.game.diag_reflect().diag_reflect().hash(), self.game.hash())

    def test_mutations(self):
        self.assertEqual(len(list(self.game.mutations())), 6)
        # for board in self.game.mutations():
        #     print(board.to_string())

    def test_take_longest_path(self):
        """
          0 1 2 3 4 5 6 7
        0 x
        1     o
        2   o
        3   o   o
        4
        5     o         o
        6         o
        7             o

        Legend:
        x -- start location
        o -- blank spaces which are reachable from x
        z -- blank spaces which are unreachable from x
        """

        blank_spaces = {(1, 2), (3, 3), (5, 2), (6, 4), (7, 6), (2, 1), (3, 1), (5, 7)}
        #blank_spaces = {(1, 2), (3, 3), (5, 2), (3, 1), (0, 1)}
        location = (0, 0)
        unreachable_spaces = take_longest_path(location, blank_spaces)
        self.assertEqual(set(), unreachable_spaces)
        max_move_count = len(blank_spaces) - len(unreachable_spaces)
        self.assertEqual(8, max_move_count)

        blank_spaces.add((0, 1))
        unreachable_spaces = take_longest_path(location, blank_spaces)
        self.assertEqual({(0, 1),}, unreachable_spaces)
        max_move_count = len(blank_spaces) - len(unreachable_spaces)
        self.assertEqual(8, max_move_count)

        blank_spaces.add((4, 5))
        unreachable_spaces = take_longest_path(location, blank_spaces)
        self.assertEqual({(0, 1),}, unreachable_spaces)
        max_move_count = len(blank_spaces) - len(unreachable_spaces)
        self.assertEqual(9, max_move_count)

        blank_spaces.add((6, 0))
        unreachable_spaces = take_longest_path(location, blank_spaces)
        self.assertEqual({(0, 1),(6, 0)}, unreachable_spaces)
        max_move_count = len(blank_spaces) - len(unreachable_spaces)
        self.assertEqual(9, max_move_count)

        blank_spaces.add((6, 7))
        unreachable_spaces = take_longest_path(location, blank_spaces)
        self.assertEqual({(0, 1), (6, 7), (6, 0)}, unreachable_spaces)
        max_move_count = len(blank_spaces) - len(unreachable_spaces)
        self.assertEqual(9, max_move_count)

        blank_spaces.add((2, 6))
        unreachable_spaces = take_longest_path(location, blank_spaces)
        self.assertEqual({(0, 1), (6, 7), (6, 0)}, unreachable_spaces)
        max_move_count = len(blank_spaces) - len(unreachable_spaces)
        self.assertEqual(10, max_move_count)

        blank_spaces.add((0, 7))
        unreachable_spaces = take_longest_path(location, blank_spaces)
        self.assertEqual({(0, 1), (6, 7), (6, 0)}, unreachable_spaces)
        max_move_count = len(blank_spaces) - len(unreachable_spaces)
        self.assertEqual(11, max_move_count)

if __name__ == '__main__':
    unittest.main()
