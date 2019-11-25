from copy import deepcopy

from util import *

NORTH_HOME = 7
SOUTH_HOME = 15


def opponent_well(my_side):
    if my_side == POSITION_NORTH:
        return SOUTH_HOME
    else:
        return NORTH_HOME


def hole_owned_by_me(my_side, hole_index):
    if my_side == POSITION_NORTH:
        return 0 <= hole_index <= 6
    else:
        return 8 <= hole_index <= 14


def start_index(side, move):
    if side == POSITION_NORTH:
        return move - 1
    else:
        return move + 7


class Board:

    def __init__(self):
        # this is how the board technically looks like
        # self.north = [0, 7, 7, 7, 7, 7, 7, 7] home north – holes north
        # self.south = [0, 7, 7, 7, 7, 7, 7, 7] home south – holes south

        # this is how it's kept in memory
        self.state = [7, 7, 7, 7, 7, 7, 7, 0, 7, 7, 7, 7, 7, 7, 7, 0]
        # holes north - home north - holes south - home south

    def update(self, board_state):
        positions = [int(x) for x in board_state.split(',')]
        self.state = positions
        self.print_board()

    def get_score_for_side(self, side):
        if side == POSITION_NORTH:
            return self.state[7]
        elif side == POSITION_SOUTH:
            return self.state[15]

    def print_board(self):
        log("Board update")

        # North side
        reversed_north = self.state[:7]
        reversed_north.reverse()
        log(str(self.state[7]) + " -- " + str(reversed_north))

        # South side
        log(str(self.state[8:15]) + " -- " + str(self.state[15]))

    # generates a new board without changing the state of current
    def generate_move(self, side, move):  # side is the side that made the move

        new_board = deepcopy(self)
        count = self.get_number_in_cell(side, move)
        index = start_index(side, move)

        # update all cells
        new_board.state[index] = 0
        while count != 0:
            index += 1
            if index == 16:
                index = 0

            if index != opponent_well(side):
                new_board.state[index] += 1
                count -= 1

        # update opposite cell if needed
        if new_board.state[index] == 1:  # last cell was 0 (incremented to 1)
            if hole_owned_by_me(side, index):  # hole I ended up is owned by me
                # take all pebbles on opposite side
                new_board.increment_home(side, new_board.state[14-index])
                new_board.state[14-index] = 0

        return new_board

    def increment_home(self, my_side, pebbles_no):
        if my_side == POSITION_NORTH:
            self.state[NORTH_HOME] += pebbles_no
        else:
            self.state[SOUTH_HOME] += pebbles_no

    def get_number_in_cell(self, side, cell):
        if 1 <= cell <= 7:
            if side == POSITION_NORTH:
                return self.state[cell - 1]
            elif side == POSITION_SOUTH:
                return self.state[cell + 7]
        else:
            log("Invalid (side, cell) combination in get_number_in_cell")

    def cell_not_empty(self, side, cell):
        return self.get_number_in_cell(side, cell) != 0
