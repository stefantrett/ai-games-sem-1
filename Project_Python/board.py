from util import log


class Board:

    def __init__(self):
        self.north = [0, 7, 7, 7, 7, 7, 7, 7]
        self.south = [0, 7, 7, 7, 7, 7, 7, 7]

    def update(self, board_state):
        positions = [int(x) for x in board_state.split(',')]

        self.north[0] = positions[7]
        self.north[1:8] = positions[:7]

        self.south[0] = positions[15]
        self.south[1:8] = positions[8:15]
        self.print_board()

    def print_board(self):
        reversed_north = self.north[1:]
        reversed_north.reverse()

        log(str(self.north[0]) + " -- " + str(reversed_north))
        log(str(self.south[1:]) + " -- " + str(self.south[0]) + '\n')
