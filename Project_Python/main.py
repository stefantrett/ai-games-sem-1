from tortellini import Tortellini
from board import Board
from util import *
import traceback

game_over = False
board = Board()
agent = Tortellini(board)
is_SWAP_an_option = False
# variable to keep the bord state of how we would move if we were the opponent
# (only used in first turn to decide if we swap)
board_we_would_get_to = None

# TODO: delete stacktrace log
try:
    while not game_over:
        command = input()
        args = command.split(';')

        if args[0] == 'START':
            if args[1] == SOUTH:
                agent.my_position, agent.opp_position = SOUTH_SIDE, NORTH_SIDE
                move = agent.make_move(agent.my_position)
                print('MOVE;{}'.format(move))
            elif args[1] == NORTH:
                agent.my_position, agent.opp_position = NORTH_SIDE, SOUTH_SIDE
                is_SWAP_an_option = True
                board_we_would_get_to = agent.simulate_move_for_side(agent.opp_position)
            else:
                log("Command not valid")

        elif args[0] == 'END':
            game_over = True

        elif args[0] == 'CHANGE':
            if args[1] == 'SWAP':
                agent.my_position, agent.opp_position = agent.opp_position, agent.my_position
                move = agent.make_move(agent.my_position)
                print('MOVE;{}'.format(move))
            else:
                board.update(args[2])
                if args[3] == 'YOU':
                    if is_SWAP_an_option:
                        is_SWAP_an_option = False
                        # decide if we should swap or not
                        if board == board_we_would_get_to:
                            agent.my_position, agent.opp_position = agent.opp_position, agent.my_position
                            print('SWAP')
                        else:
                            move = agent.make_move(agent.my_position)
                            print('MOVE;{}'.format(move))
                    else:
                        move = agent.make_move(agent.my_position)
                        print('MOVE;{}'.format(move))
except Exception as e:
    log(traceback.extract_tb(e.__traceback__))
    log(e)


# ============ TESTING AREA ============
def generate_board():
    initial = Board()

    for move in range(1, 8):
        new_board, _ = initial.generate_move(SOUTH_SIDE, move)
        new_board.print_board()
