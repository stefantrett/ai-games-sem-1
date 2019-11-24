from util import log


class Board:

    def __init__(self):
        self.north = [7, 7, 7, 7, 7, 7, 7, 0]
        self.south = [7, 7, 7, 7, 7, 7, 7, 0]

    def update(self, board_state):
        positions = board_state.split(',')
        self.north = positions[:8]
        self.south = positions[8:]
        self.print_board()

    def print_board(self):
        reversed_north = self.north[:7]
        reversed_north.reverse()

        log(str(self.north[7]) + " -- " + str(reversed_north) + '\n')
        log(str(self.south[:7]) + " -- " + str(self.south[7]) + '\n\n')
