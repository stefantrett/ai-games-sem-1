from .tortellini import Tortellini
from .board import Board

POSITION_SOUTH = 'South'
POSITION_NORTH = 'North'

game_over = True
board = Board()
agent = Tortellini(board)

while not game_over:
    command = input()
    args = command.split(';')

    if args[0] == 'START':
        if args[1] == POSITION_SOUTH:
            agent.my_position = POSITION_SOUTH
            agent.opp_position = POSITION_NORTH
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


