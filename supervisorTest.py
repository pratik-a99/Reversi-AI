from reversi import *
import importlib
import sys
import time


# How to call function from a programname in runtime
# https://stackoverflow.com/a/58733987/5911854
def get_func(programname, functionname):
    module_str = programname
    module = importlib.import_module(module_str)  # import module from str
    f = getattr(module, functionname)  # get function "function" in module
    return f


def showPoints1(mainBoard, player1Tile, player2Tile):
    # Prints out the current score.
    scores = getScoreOfBoard(mainBoard)
    print('Player 1 :%s points. Player 2 :%s points.' %
          (scores[player1Tile], scores[player2Tile]))


# import threading
# alarm=None

# def terminator(terminator_args):
#     terminator_args.append("TimeOut")
#     alarm.cancel()

# def timed_execute(timeout_limit, func, args):
#     global alarm

#     ret=None
#     terminator_args=[]
#     alarm = threading.Timer(timeout_limit, terminator, args=[terminator_args])
#     alarm.start()
#     ret = func(*args)
#     alarm.cancel()

#     if len(terminator_args)>0:
#         print("Function "+ func.__name__ + " timed out") # continue the for loop if function A takes more than 5 second
#         ret="TimeOut"

#     return ret


#########################################################################################

def supervisor(prog1_name, prog2_name, TIMEOUT_LIMIT=1, verbose=True):
    player1_get_move = get_func(prog1_name, 'get_move')
    player2_get_move = get_func(prog2_name, 'get_move')

    if prog1_name == prog2_name:
        prog1_name = prog1_name+"_v1"
        prog2_name = prog2_name+"_v2"

    moves = 0

    mainBoard = getNewBoard()
    resetBoard(mainBoard)
    player1Tile, player2Tile = ['X', 'O']
    turn = prog1_name
    while True:
        if turn == prog1_name:
            if verbose:
                drawBoard(mainBoard)
            showPoints1(mainBoard, player1Tile, player2Tile)
            while True:
                #move = player1_get_move(mainBoard, player1Tile)
                start = time.time()
                while time.time() - start < TIMEOUT_LIMIT:
                    move = player1_get_move(mainBoard, player1Tile)

                if isValidMove(mainBoard, player1Tile, move[0], move[1]):
                    break
                else:
                    print(str(move[0])+str(move[1]) + "is an invalid move")
            print("Player 1 played:["+str(move[0]+1)+","+str(move[1]+1)+"]")
            makeMove(mainBoard, player1Tile, move[0], move[1])

            if getValidMoves(mainBoard, player2Tile) == []:
                break
            else:
                turn = prog2_name

        else:
            if verbose:
                drawBoard(mainBoard)
            showPoints1(mainBoard, player1Tile, player2Tile)

            while True:
                # move = player2_get_move(mainBoard, player2Tile)
                start = time.time()
                while time.time() - start < TIMEOUT_LIMIT:
                    move = player2_get_move(mainBoard, player2Tile)

                if isValidMove(mainBoard, player2Tile, move[0], move[1]):
                    break
                else:
                    print(str(move[0])+str(move[1]) + "is an invalid move")
            print("Player 2 played:["+str(move[0]+1)+","+str(move[1]+1)+"]")
            makeMove(mainBoard, player2Tile, move[0], move[1])

            if getValidMoves(mainBoard, player1Tile) == []:
                break
            else:
                turn = prog1_name

        moves += 1
    # Display the final score.
    drawBoard(mainBoard)
    scores = getScoreOfBoard(mainBoard)
    print('Player 1 scored %s points. Player 2 scored %s points.' %
          (scores[player1Tile], scores[player2Tile]))
    if scores[player1Tile] > scores[player2Tile]:
        print('Player 1 wins by %s points in %s moves!' %
              (scores[player1Tile] - scores[player2Tile], moves))
        return ("p1")
    elif scores[player1Tile] < scores[player2Tile]:
        print('Player 2 wins by %s points in %s moves!' %
              (scores[player2Tile] - scores[player1Tile], moves))
        return ("p2")
    else:
        print('The game was a tie in %s moves!' % (moves))
        return ("tie")


if __name__ == "__main__":
    TIMEOUT_LIMIT = 0.5
    verbose = True
    if len(sys.argv) < 3:
        print(
            "You need to provide 2 inputs program. One or both of them can be \"computer\"")
        quit()
    prog1_name = sys.argv[1]
    prog2_name = sys.argv[2]
    if len(sys.argv) > 3:
        TIMEOUT_LIMIT = float(sys.argv[3])
    if len(sys.argv) > 4:
        verbose = int(sys.argv[4])

    sm = supervisor(prog1_name, prog2_name,
                    TIMEOUT_LIMIT=TIMEOUT_LIMIT, verbose=verbose)
