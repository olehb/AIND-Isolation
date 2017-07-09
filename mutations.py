def transform_state(transformer, state, width):
    """
    This function takes board state and trasforms it.
    Example transformations: rotate 90 degrees, flip diagonally
    """
    # Mutating game board
    # 3 last elements of the "state" contains player's info,
    # thus have to be transformed separately.
    transformed_state = [state[transformer(i, width)] for i in range(len(state)-3)]
    # Transforming player states accordingly
    for i in range(-3, 0):
        transformed_state.append(transformer(state[i], width))
    return transformed_state

def hash_state(state):
    return str(state).__hash__()

def get_transformations_hashes(game):
    """
    Returns hashes for transformed board states.
    """
    yield game.hash()
    width = game.width
    # Flip game board diagonally
    diag = lambda i, w: (i%w)*w + i//w if i is not None else None
    # Rotate game board
    rot = lambda i, w: (w - 1 -(i%w))*w + i//w if i is not None else None
    transformed_state = game._board_state
    # Otherwise it's failing with "Exception: unsupported operand type(s) for %: 'NoneType' and 'int'"
    if transformed_state is None or width is None:
        return
    for _ in range(3):
        yield hash_state(transform_state(diag, transformed_state, width))
        transformed_state = transform_state(rot, transformed_state, width)
        yield hash_state(transformed_state)
