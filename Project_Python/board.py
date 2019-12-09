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
        # holes north - home north - holes south - home south
        self.state = [7, 7, 7, 7, 7, 7, 7, 0, 7, 7, 7, 7, 7, 7, 7, 0]

        # Last position move for each side
        self.last_position_moved = None

    def __eq__(self, other):
        # Overrides the default implementation
        if isinstance(other, Board):
            return self.state == other.state
        return False

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

                # move the capturing pebble as well
                new_board.increment_well(side, new_board.state[14 - index] + 1)
                new_board.state[index] = 0
                new_board.state[14 - index] = 0

        if index == my_well(side):
            ended_in_own_well = True

        new_board.last_position_moved = move

        return new_board, ended_in_own_well

    def get_evaluation_backup(self, maximizing_player):
        # Heuristic 1
        left_most_pit_score = self.state[0] - self.state[8]

        # Heuristic 2
        pits_score = sum(self.state[0:7]) - sum(self.state[8:15])

        # Heuristic 3
        number_of_possible_moves = sum(cell > 0 for cell in self.state[0:7]) - sum(
            cell > 0 for cell in self.state[8:15])

        # Heuristic 4
        well_points = self.get_well_score(NORTH_SIDE) - self.get_well_score(SOUTH_SIDE)

        # Heuristic 5
        if maximizing_player is True and self.last_position_moved == 7:
            right_most_position = 1
        elif maximizing_player is False and self.last_position_moved == 7:
            right_most_position = -1
        else:
            right_most_position = 0

        return (left_most_pit_score * left_most_pit_score_weight) + (
                pits_score * pits_score_weight) + (
                       number_of_possible_moves * number_of_possible_moves_weight) + (
                       well_points * well_points_weight) + (
                       right_most_position * right_most_position_weight)

    def get_evaluation(self, side):
        evaluation = 0.0

        stones_in_north_well = self.get_well_score(NORTH_SIDE)
        stones_in_south_well = self.get_well_score(SOUTH_SIDE)

        if stones_in_north_well != 0 or stones_in_south_well != 0:
            if stones_in_north_well != stones_in_south_well:
                if stones_in_north_well > stones_in_south_well:
                    max_well_stones, min_well_stones = stones_in_north_well, stones_in_south_well
                else:
                    min_well_stones, max_well_stones = stones_in_north_well, stones_in_south_well

                evaluation = (1.0 / max_well_stones * (max_well_stones - min_well_stones) + 1.0) * max_well_stones

                if stones_in_north_well <= stones_in_south_well:
                    evaluation *= -1.0

        for i in range(1, 8):
            if self.get_cell_score(side, i) == 0 and self.can_be_filled(side, i):
                evaluation += self.get_cell_score(opposite_side(side), i) / 2

        for i in range(1, 8):
            if self.get_cell_score(opposite_side(side), i) == 0 and self.can_be_filled(opposite_side(side), i):
                evaluation -= self.get_cell_score(side, i) / 2

        for i in range(1, 8):
            if 7 - i + 1 == self.get_cell_score(side, i):
                evaluation += 1.0

        own_pits_score = 0.0
        for i in range(1, 8):
            own_pits_score += self.get_cell_score(side, i)

        opp_pits_score = 0.0
        for i in range(1, 8):
            opp_pits_score += self.get_cell_score(opposite_side(side), i)

        pits_score_eval = (own_pits_score - opp_pits_score) / 2
        evaluation += pits_score_eval

        return evaluation

    def can_be_filled(self, side, n):
        can_be = False

        for i in range(n-1, 0):
            if n - i == self.get_cell_score(side, i):
                can_be = True
                break

        return can_be

    def get_pits_score_for_sides(self):
        return sum(self.state[0:7]), sum(self.state[8:15])

    def get_number_of_possible_moves_for_sides(self):
        return sum(cell > 0 for cell in self.state[0:7]), sum(cell > 0 for cell in self.state[8:15])

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
