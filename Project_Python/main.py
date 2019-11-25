from tortellini import Tortellini
from board import Board
from util import *

game_over = False
board = Board()
agent = Tortellini(board)

while not game_over:
    command = input()
    args = command.split(';')

    if args[0] == 'START':
        if args[1] == POSITION_SOUTH:
            agent.my_position = POSITION_SOUTH
            agent.opp_position = POSITION_NORTH
            agent.make_move()
        elif args[1] == POSITION_NORTH:
            agent.my_position = POSITION_NORTH
            agent.opp_position = POSITION_SOUTH

    elif args[0] == 'END':
        game_over = True

    elif args[0] == 'CHANGE':
        if args[1] == 'SWAP':
            agent.my_position, agent.opp_position = agent.opp_position, agent.my_position
        else:
            board.update(args[2])
            if args[3] == 'YOU':
                agent.make_move()


# ============ TESTING AREA ============
def generate_board():
    initial = Board()

    for move in range(1, 8):
        new_board = initial.generate_move(POSITION_SOUTH, move)
        new_board.print_board()

