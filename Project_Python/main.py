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
        if args[1] == SOUTH:
            agent.my_position, agent.opp_position = SOUTH_SIDE, NORTH_SIDE
            agent.make_move()
        elif args[1] == NORTH:
            agent.my_position, agent.opp_position = NORTH_SIDE, SOUTH_SIDE
        else:
            log("Command not valid")

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
        new_board = initial.generate_move(SOUTH_SIDE, move)
        new_board.print_board()

