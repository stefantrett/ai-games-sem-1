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
    number_of_arguments = len(args)

    if not args[0]:
        print("Invalid command")
    elif args[0] == 'END':
        game_over = True
    elif args[0] == 'START':
        if args[1] == 'South':
            agent.position = POSITION_SOUTH
            agent.opponent_position = POSITION_NORTH
        elif args[1] == 'North':
            agent.position = POSITION_NORTH
            agent.position = POSITION_SOUTH
        else:
            pass
    # ======================================================================
    elif args[0] == 'CHANGE':
        if args[1] == 'SWAP':
            agent.position, agent.opponent_position = agent.opponent_position, agent.position
        else:
            board.update()

