from util import *


class Board:

    def __init__(self):
        # this is how the board technically looks like
        # self.north = [0, 7, 7, 7, 7, 7, 7, 7] home north – holes north
        # self.south = [0, 7, 7, 7, 7, 7, 7, 7] home south – holes south

        # this is how it's kept in memory
        self.board = [7, 7, 7, 7, 7, 7, 7, 0, 7, 7, 7, 7, 7, 7, 7, 0] # holes north - home north - holes south - home south

    def update(self, board_state):
        positions = [int(x) for x in board_state.split(',')]
        self.board = positions
        self.print_board()

    def cell_not_empty(self, side, cell):
        if 1 <= cell <= 7:
            if side == POSITION_NORTH:
                return self.board[cell - 1] != 0
            elif side == POSITION_SOUTH:
                return self.board[cell + 7] != 0
        else:
            log("Invalid (side, cell) combination in cell_not_empty")

    def print_board(self):
        log("Board update")

        # North side
        reversed_north = self.board[:7]
        reversed_north.reverse()
        log(str(self.board[7]) + " -- " + str(reversed_north))

        # South side
        log(str(self.board[8:15]) + " -- " + str(self.board[15]))

    # generates a new board without changing the state of current
    # TODO: also implement for case where cell is empty and you take all opposite pebbles
    def generate_move(self, side, move):
        if 1 <= move <= 7:  # check move is valid
            if side == POSITION_NORTH:  # move for North
                # count = self.north[move]
                pass

            elif side == POSITION_SOUTH:  # move for South
                # move for South
                pass
        else:
            log("Invalid move")
