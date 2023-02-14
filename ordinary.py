# I pledge on my honor that I have not given or received
# any unauthorized assistance on this project.
# Pratik Acharya

import math
import random
from reversi import *


def ucb_choose(board, tile):
    """ Returns the child with the highest UCB score

    Args:
        board (list): The board
        tile (str): The tile

    Returns:
        tuple: The child with the highest UCB score

    """

    # global SEEN
    # global REWARDS
    # global TIMES
    # global MYTILE

    # Normalize rewards between 0 and 1
    if (max(REWARDS.values()) - min(REWARDS.values())) == 0:
        pass
    else:
        for key in REWARDS:
            REWARDS[key] = (REWARDS[key] - min(REWARDS.values())) / \
                (max(REWARDS.values()) - min(REWARDS.values()))

    original_board = getBoardCopy(board)
    original_tile = tile

    valid_moves = getValidMoves(board, tile)

    copied_board = getBoardCopy(board)

    not_seen = []

    # Get the valid moves that have not been seen

    for move_i in valid_moves:
        makeMove(copied_board, tile, move_i[0], move_i[1])
        if not (copied_board, tile) in SEEN:
            # notSeen = np.append(notSeen, (copiedBoard, tile))
            not_seen.append((copied_board, tile))
        copied_board = getBoardCopy(original_board)

    # If there are unseen moves, choose one of them

    if not_seen:
        # print(notSeen)
        return_move = random.choice(not_seen)
        return return_move[0], return_move[1]

    # If all moves have been seen, choose the move with the highest UCB score
    else:

        copied_board = getBoardCopy(original_board)

        tries_sum = 0

        for move_i in valid_moves:
            makeMove(copied_board, tile, move_i[0], move_i[1])
            tries_sum += TIMES[(str(copied_board), tile)]
            copied_board = getBoardCopy(original_board)

        # triesSum = np.sum(times.values())

        if original_tile == MYTILE:
            max_ucb = -1
            copied_board = getBoardCopy(original_board)
            for move_i in valid_moves:
                makeMove(copied_board, tile, move_i[0], move_i[1])
                ucb = REWARDS[(str(copied_board), tile)] + math.sqrt(2 *
                                                                     math.log(tries_sum) / TIMES[(str(copied_board), tile)])
                if ucb > max_ucb:
                    max_ucb = ucb
                    return_move = (copied_board, tile)
                copied_board = getBoardCopy(original_board)
        else:
            max_ucb = -1
            copied_board = getBoardCopy(original_board)
            for move_i in valid_moves:
                makeMove(copied_board, tile, move_i[0], move_i[1])
                ucb = 1 - REWARDS[(str(copied_board), tile)] + math.sqrt(2 *
                                                                         math.log(tries_sum) / TIMES[(str(copied_board), tile)])
                if ucb > max_ucb:
                    max_ucb = ucb
                    return_move = (copied_board, tile)
                copied_board = getBoardCopy(original_board)

        return return_move[0], return_move[1]


def uct(board, tile):
    """ Returns value of board after UCT search

    Args:
        board (list): The board
        tile (str): The tile

    Returns:
        int: The value of the board

    """

    # global SEEN
    # global REWARDS
    # global TIMES
    # global MYTILE

    tiles = ['X', 'O']

    og_board = getBoardCopy(board)
    og_tile = tile

    value = 0

    # Check if the move is seen or not

    if (og_board, og_tile) in SEEN:
        pass
    else:
        # seen = np.append(seen, (board, tile))
        SEEN.append((og_board, og_tile))
        REWARDS[(str(og_board), og_tile)] = 0
        TIMES[(str(og_board), og_tile)] = 0

    # Get the opponent's tile for the next move

    if tiles[0] == tile:
        opposite_tile = tiles[1]
    else:
        opposite_tile = tiles[0]

    # Get the opponent's tile for the whole game

    if tiles[0] == MYTILE:
        opponent_tile = tiles[1]
    else:
        opponent_tile = tiles[0]

    if not getValidMoves(board, tile):
        result = getScoreOfBoard(board)

        # print(result)
        # print(myTile)

        if result[MYTILE] > result[opponent_tile]:
            value = 1
        elif result[MYTILE] < result[opponent_tile]:
            value = 0
    else:
        new_board, _ = ucb_choose(board, tile)
        value = uct(new_board, opposite_tile)

    # if (str(board), tile) in rewards.keys():
    reward = REWARDS[(str(og_board), og_tile)]
    REWARDS[(str(og_board), og_tile)] = (reward + value) / \
        (TIMES[(str(og_board), og_tile)] + 1)
    TIMES[(str(og_board), og_tile)] += 1

    return value


def get_move(board, tile):
    """ Returns the move that the UCT algorithm wants to make

    Args:
        board (list): The board
        tile (str): The tile

    Returns:
        tuple: The move that the UCT algorithm wants to make

    """

    if 'seen' not in globals():
        global SEEN
        global REWARDS
        global TIMES
        global MYTILE
        global oldBoard

        SEEN = []
        REWARDS = {}
        TIMES = {}
        MYTILE = tile
        oldBoard = getBoardCopy(board)

    if oldBoard != board:
        SEEN = []
        REWARDS = {}
        TIMES = {}
        MYTILE = tile

    board_original = getBoardCopy(board)

    _ = uct(board, tile)
    board = board_original

    valid_moves_orig = getValidMoves(board, tile)

    # Randomize the order of the valid moves
    random.shuffle(valid_moves_orig)

    max_q = -1
    copied_board = getBoardCopy(board_original)

    return_move = None

    tiles = ['X', 'O']

    if tiles[0] == tile:
        opposite_tile = tiles[1]
    else:
        opposite_tile = tiles[0]

    for move_itr in valid_moves_orig:
        makeMove(copied_board, tile, move_itr[0], move_itr[1])
        if ((str(copied_board), opposite_tile) in REWARDS.keys()):
            if (REWARDS[(str(copied_board), opposite_tile)] > max_q):
                max_q = REWARDS[(str(copied_board), opposite_tile)]
                return_move = move_itr
        copied_board = getBoardCopy(board_original)

    oldBoard = getBoardCopy(board_original)

    return return_move
