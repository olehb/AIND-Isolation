"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""

from random import random

_MAX_SCORE = float("+inf")
_MIN_SCORE = float("-inf")
_DELIM = '>'

"""
Experimentally determined number of average moves per game,
depending on board size, e.g. it takes ~35.5 moves to play on 7x7 board
"""
_AVG_MOVES = {49: 35.5}


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_winner(player):
        return _MAX_SCORE
    if game.is_loser(player):
        return _MIN_SCORE

    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))

    return float(len(own_moves) - (1+random())*len(opp_moves))


def custom_score_2(game, player):
    """
    Calculates score based on partitions

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_winner(player):
        return _MAX_SCORE
    if game.is_loser(player):
        return _MIN_SCORE

    blank_spaces = game.get_blank_spaces()
    if len(blank_spaces) <= game.width*game.height/2:
        own_location = game.get_player_location(player)
        own_unreachable_spaces = check_partition(own_location, set(blank_spaces))
        opp_location = game.get_player_location(game.get_opponent(player))
        opp_unreachable_spaces = check_partition(opp_location, set(blank_spaces))
        if opp_unreachable_spaces != own_unreachable_spaces:
            if not opp_unreachable_spaces & own_unreachable_spaces:
                if len(opp_unreachable_spaces) > len(own_unreachable_spaces):
                    return _MAX_SCORE
                return _MIN_SCORE
            return 10*(len(opp_unreachable_spaces) - len(own_unreachable_spaces))
    return custom_score_3(game, player)


def check_partition(location, blank_spaces):
    """
    Check if all available blank spaces
    """
    for move in get_moves(location, blank_spaces):
        blank_spaces.remove(move)
        check_partition(move, blank_spaces)
    return blank_spaces



def get_moves(move, blank_spaces):
    """
    Get available moves within given blank spaces
    """
    r, c = move
    directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                  (1, -2), (1, 2), (2, -1), (2, 1)]
    moves = [(r + dr, c + dc) for dr, dc in directions]
    return filter(lambda m: m in blank_spaces, moves)


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_winner(player):
        return _MAX_SCORE
    if game.is_loser(player):
        return _MIN_SCORE

    average_moves = _AVG_MOVES.get(game.width*game.height, game.move_count)
    border_move_discount = 0.5 + game.move_count/average_moves
    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))

    return float(len(own_moves)-border_move_discount*num_border_moves(own_moves, game)
                 - len(opp_moves)+border_move_discount*num_border_moves(opp_moves, game))

def num_border_moves(moves, game):
    return sum(1 for move in moves
               if move[0] in [0, game.height-1]
               or move[1] in [0, game.width-1])

def mutate_state(mutator, state, width):
    # Mutating game board
    mutated_state = [state[mutator(i, width)] for i in range(len(state)-3)]
    # Transforming player states accordingly
    for i in range(-3, 0):
        mutated_state.append(mutator(state[i], width))
    return mutated_state

def hash_state(state):
    return str(state).__hash__()

def get_mutation_hashes(game):
    yield game.hash()
    width = game.width
    diag = lambda i, w: (i%w)*w + i//w if i is not None else None
    rot = lambda i, w: (w - 1 -(i%w))*w + i//w if i is not None else None
    mutated_state = game._board_state
    # Otherwise it's failing with "Exception: unsupported operand type(s) for %: 'NoneType' and 'int'"
    if mutated_state is None or width is None:
        return
    for _ in range(3):
        yield hash_state(mutate_state(diag, mutated_state, width))
        mutated_state = mutate_state(rot, mutated_state, width)
        yield hash_state(mutated_state)


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    NO_MOVE = (-1, -1)

    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def check_time(self):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = self.NO_MOVE

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        self.check_time()

        _, best_move = self._max_value(game, game.active_player, depth)
        # Uncomment lines below to never forfeit the game
        if best_move == self.NO_MOVE and len(game.get_legal_moves()) > 0:
            return game.get_legal_moves()[0]
        return best_move

    def _max_value(self, game, player, plies_left):
        self.check_time()
        best_move = self.NO_MOVE
        best_score = _MIN_SCORE
        try:
            for move in game.get_legal_moves():
                current_game = game.forecast_move(move)
                if plies_left <= 1:
                    current_score = self.score(current_game, player)
                else:
                    current_score, _ = self._min_value(current_game,
                                                       player, plies_left-1)
                if current_score > best_score:
                    best_score = current_score
                    best_move = move
        except SearchTimeout:
            pass
        return best_score, best_move

    def _min_value(self, game, player, plies_left):
        self.check_time()
        best_move = self.NO_MOVE
        best_score = _MAX_SCORE
        try:
            for move in game.get_legal_moves():
                current_game = game.forecast_move(move)
                if plies_left <= 1:
                    current_score = self.score(current_game, player)
                else:
                    current_score, _ = self._max_value(current_game,
                                                       player, plies_left-1)
                if current_score < best_score:
                    best_score = current_score
                    best_move = move
        except SearchTimeout:
            pass
        return best_score, best_move


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left
        best_move = self.NO_MOVE

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            for depth in range(game.width*game.height):
                move = self.alphabeta(game, depth+1)
                if move != self.NO_MOVE:
                    best_move = move
        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def alphabeta(self, game, depth, alpha=_MIN_SCORE, beta=_MAX_SCORE):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        self.check_time()
        _, best_move = self._max_value(game, game.active_player, depth,
                                       alpha, beta)
        return best_move

    def _max_value(self, game, player, plies_left, alpha, beta):
        self.check_time()
        log = get_log(plies_left, 'MAX')
        best_move = self.NO_MOVE
        best_score = _MIN_SCORE
        moves = game.get_legal_moves()
        # log(f"legal moves {moves}")
        for move in moves:
            current_game = game.forecast_move(move)

            if plies_left <= 1:
                current_score = self.score(current_game, player)
            else:
                current_alpha = max(best_score, alpha)
                current_score, _ = self._min_value(current_game,
                                                   player, plies_left-1,
                                                   current_alpha, beta)
            if current_score > best_score:
                best_score = current_score
                best_move = move
            if best_score >= beta:
                # log(f"{move} beta={beta}, best_score={best_score} cutting off...")
                break
        # log(f"{best_move} -> {best_score}")
        return best_score, best_move

    def _min_value(self, game, player, plies_left, alpha, beta):
        self.check_time()
        log = get_log(plies_left, 'MIN')
        best_move = self.NO_MOVE
        best_score = _MAX_SCORE
        moves = game.get_legal_moves()
        # log(f"legal moves {moves}")
        for move in moves:
            current_game = game.forecast_move(move)
            if plies_left <= 1:
                current_score = self.score(current_game, player)
            else:
                current_beta = min(best_score, beta)
                current_score, _ = self._max_value(current_game,
                                                   player, plies_left-1,
                                                   alpha, current_beta)
            if current_score < best_score:
                best_score = current_score
                best_move = move
            if best_score <= alpha:
                # log(f"{move} alpha={alpha}, best_score={best_score} cutting off...")
                break
        # log(f"{best_move} -> {best_score}")
        return best_score, best_move

def get_log(intend, prefix):
    def log(msg):
        pass
        # print('>'*intend+f' {prefix} '+msg)
    return log
