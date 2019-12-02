from copy import deepcopy

from util import *

NORTH_HOME = 7
SOUTH_HOME = 15

# my_side == NORTH_SIDE (= 0) -> 1 - my_side * result (if you want result for NORTH)
# my_side == SOUTH_HOME (= 1) -> my_side * result (if you want result for SOUTH)


def my_well(my_side):
    return (1 - my_side) * NORTH_HOME + my_side * SOUTH_HOME


def opponent_well(my_side):
    return my_side * NORTH_HOME + (1 - my_side) * SOUTH_HOME


def owned_hole(my_side, hole_index):
    return 0 <= hole_index <= 6 if my_side == NORTH_SIDE else 8 <= hole_index <= 14


def get_index(side, move):
    if 1 <= move <= 7:
        return (1 - side) * (move - 1) + side * (move + 7)
    else:
        log("Cannot get index out of (side, move) combination")


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

    # generates a new board without changing the state of current
    # side = the side that made the move
    def generate_move(self, side, move):
        new_board = deepcopy(self)
        count = self.get_cell_score(side, move)
        index = get_index(side, move)
        new_board.state[index] = 0
        ended_in_own_well = False

        # update all cells
        while count != 0:
            index = 0 if index == 15 else index + 1  # cycle around

            if index != opponent_well(side):  # if it isn't opponent's well
                new_board.state[index] += 1
                count -= 1

        # opposite cell - special case
        if new_board.state[index] == 1:  # if last cell was 0 before increment (incremented to 1)
            if owned_hole(side, index):  # hole I ended up on is owned by me
                # take all pebbles on opposite side
                new_board.increment_well(side, new_board.state[14 - index])
                new_board.state[14 - index] = 0

        if index == my_well(index):
            ended_in_own_well = True

        return new_board, ended_in_own_well

    def get_evaluation(self):
        return self.get_well_score(NORTH_SIDE) - self.get_well_score(SOUTH_SIDE)

    def get_well_score(self, side):
        return self.state[my_well(side)]

    def increment_well(self, side, pebbles_no):
        self.state[my_well(side)] += pebbles_no

    def get_cell_score(self, side, cell):
        return self.state[get_index(side, cell)]

    def cell_not_empty(self, side, cell):
        return self.get_cell_score(side, cell) != 0

    def no_moves_left(self, side):
        return max(self.state[0:7]) == 0 if side == NORTH_SIDE else max(self.state[8:15]) == 0

    def print_board(self):
        log("Board update")

        # North side
        reversed_north = self.state[0:7]
        reversed_north.reverse()
        log(str(self.state[NORTH_HOME]) + " -- " + str(reversed_north))

        # South side
        log(str(self.state[8:15]) + " -- " + str(self.state[SOUTH_HOME]))

