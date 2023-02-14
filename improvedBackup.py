from reversi import *
import numpy as np
import random
import math


def UCBChoose(board, tile):
    """ Returns the child with the highest UCB score

    Args:
        board (list): The board
        tile (str): The tile

    Returns:
        tuple: The child with the highest UCB score

    """

    global seen
    global rewards
    global times
    global myTile

    # Normalize rewards between 0 and 1
    if (max(rewards.values()) - min(rewards.values())) == 0:
        pass
    else:
        for key in rewards:
            rewards[key] = (rewards[key] - min(rewards.values())) / \
                (max(rewards.values()) - min(rewards.values()))

    originalBoard = getBoardCopy(board)
    originalTile = tile

    validMoves = getValidMoves(board, tile)

    copiedBoard = getBoardCopy(board)

    notSeen = []

    # Get the valid moves that have not been seen
    for move in validMoves:
        makeMove(copiedBoard, tile, move[0], move[1])
        if not (copiedBoard, tile) in seen:
            # notSeen = np.append(notSeen, (copiedBoard, tile))
            notSeen.append((copiedBoard, tile))
        copiedBoard = getBoardCopy(originalBoard)

    # If there are unseen moves, choose one of them
    if notSeen != []:
        returnMove = random.choice(notSeen)
        return returnMove[0], returnMove[1]

    # If all moves have been seen, choose the move with the highest UCB score
    else:

        copiedBoard = getBoardCopy(originalBoard)

        triesSum = 0

        for move in validMoves:
            makeMove(copiedBoard, tile, move[0], move[1])
            triesSum += times[(str(copiedBoard), tile)]
            copiedBoard = getBoardCopy(originalBoard)

        # Improvement in the code
        # triesSum = np.sum(times.values())

        if originalTile == myTile:
            maxUCB = -1
            copiedBoard = getBoardCopy(originalBoard)
            for move in validMoves:
                makeMove(copiedBoard, tile, move[0], move[1])
                UCB = rewards[(str(copiedBoard), tile)] + math.sqrt(1 *
                                                                    math.log(triesSum) / times[(str(copiedBoard), tile)])
                if UCB > maxUCB:
                    maxUCB = UCB
                    returnMove = (copiedBoard, tile)
                copiedBoard = getBoardCopy(originalBoard)
        else:
            maxUCB = -1
            copiedBoard = getBoardCopy(originalBoard)
            for move in validMoves:
                makeMove(copiedBoard, tile, move[0], move[1])
                UCB = 1 - rewards[(str(copiedBoard), tile)] + math.sqrt(1 *
                                                                        math.log(triesSum) / times[(str(copiedBoard), tile)])
                if UCB > maxUCB:
                    maxUCB = UCB
                    returnMove = (copiedBoard, tile)
                copiedBoard = getBoardCopy(originalBoard)

        return returnMove[0], returnMove[1]


def UCT(board, tile):
    """ Returns value of board after UCT search

    Args:
        board (list): The board
        tile (str): The tile

    Returns:
        int: The value of the board

    """

    global seen
    global rewards
    global times
    global myTile

    tiles = ['X', 'O']

    ogBoard = getBoardCopy(board)
    ogTile = tile

    v = 0

    # Check if the move is seen or not

    if (ogBoard, ogTile) in seen:
        pass
    else:
        # seen = np.append(seen, (board, tile))
        seen.append((ogBoard, ogTile))
        rewards[(str(ogBoard), ogTile)] = 0
        times[(str(ogBoard), ogTile)] = 0

    # Get the opponent's tile for the next move

    if tiles[0] == tile:
        oppositeTile = tiles[1]
    else:
        oppositeTile = tiles[0]

    # Get the opponent's tile for the whole game

    if tiles[0] == myTile:
        opponentTile = tiles[1]
    else:
        opponentTile = tiles[0]

    if getValidMoves(board, tile) == []:
        result = getScoreOfBoard(board)

        if result[myTile] > result[opponentTile]:
            v = 1
        elif result[myTile] < result[opponentTile]:
            v = 0
    else:
        newBoard, _ = UCBChoose(board, tile)
        v = UCT(newBoard, oppositeTile)

    # if (str(board), tile) in rewards.keys():
    reward = rewards[(str(ogBoard), ogTile)]
    rewards[(str(ogBoard), ogTile)] = (reward + v) / \
        (times[(str(ogBoard), ogTile)] + 1)
    times[(str(ogBoard), ogTile)] += 1

    return v


def get_move(board, tile):

    # check if gloabl variables are initialized
    if 'seen' not in globals():
        global seen
        global rewards
        global times
        global myTile
        global oldBoard

        seen = []
        rewards = {}
        times = {}
        myTile = tile
        oldBoard = getBoardCopy(board)

    if oldBoard != board:
        seen = []
        rewards = {}
        times = {}
        myTile = tile

    boardOriginal = getBoardCopy(board)

    v = UCT(board, tile)
    board = boardOriginal

    validMovesOrig = getValidMoves(board, tile)

    # Randomize the order of the valid moves
    random.shuffle(validMovesOrig)

    maxQ = -1
    copiedBoard = getBoardCopy(boardOriginal)

    returnMove = None
    # print(rewards.values())

    tiles = ['X', 'O']

    if tiles[0] == tile:
        oppositeTile = tiles[1]
    else:
        oppositeTile = tiles[0]

    for move in validMovesOrig:
        makeMove(copiedBoard, tile, move[0], move[1])
        # print((str(copiedBoard), tile))
        if ((str(copiedBoard), oppositeTile) in rewards.keys()):
            if (rewards[(str(copiedBoard), oppositeTile)] > maxQ):
                maxQ = rewards[(str(copiedBoard), oppositeTile)]
                returnMove = move
            # print(maxQ)
        copiedBoard = getBoardCopy(boardOriginal)

    # print(times.values())

    oldBoard = getBoardCopy(boardOriginal)

    return returnMove
