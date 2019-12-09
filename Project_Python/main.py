from copy import deepcopy
import math
import traceback
from heapq import heappop, heappush
import random

NORTH_HOME = 7
SOUTH_HOME = 15
NORTH = 'North'
SOUTH = 'South'

NORTH_SIDE = 0
SOUTH_SIDE = 1

DEPTH = 10

log_file = open("log.txt", "w")

# Heuristic 1 Weight
left_most_pit_score_weight = 0.70
# Heuristic 2 Weight
pits_score_weight = 0.85
# Heuristic 3 Weight
number_of_possible_moves_weight = 0.3
# Heuristic 4 Weight
well_points_weight = 2.0
# Heuristic 5 Weight
right_most_position_weight = 0.6


def log(some_object):
    log_file.write(str(some_object) + '\n')


def opposite_side(my_side):
    return 1 - my_side


def my_well(my_side):
    return (1 - my_side) * NORTH_HOME + my_side * SOUTH_HOME


def opponent_well(my_side):
    return my_side * NORTH_HOME + (1 - my_side) * SOUTH_HOME


def owned_hole(my_side, hole_index):
    return 0 <= hole_index <= 6 if my_side == NORTH_SIDE else 8 <= hole_index <= 14


def get_index(side, main_move):
    if 1 <= main_move <= 7:
        return (1 - side) * (main_move - 1) + side * (main_move + 7)
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
    def generate_move(self, side, board_move):
        new_board = deepcopy(self)
        count = self.get_cell_score(side, board_move)
        index = get_index(side, board_move)
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

        new_board.last_position_moved = board_move

        return new_board, ended_in_own_well

    def get_evaluation(self, maximizing_player):
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


class Tortellini:

    def __init__(self, tortellini_board):
        self.board = tortellini_board
        self.my_position = SOUTH_SIDE
        self.opp_position = NORTH_SIDE
        self.first_turn = False

    def make_move(self, side):
        if side == NORTH_SIDE:
            maximizing = True
        else:
            maximizing = False

        return self.min_max_alg(deepcopy(self.board), DEPTH, -math.inf, math.inf, maximizing, side)[1]

    def simulate_move_for_side(self, side):
        if side == NORTH_SIDE:
            maximizing = True
        else:
            maximizing = False

        tortellini_move = self.min_max_alg(Board(), DEPTH, -math.inf, math.inf, maximizing, side)[1]
        new_board_state, _ = Board().generate_move(side, tortellini_move)
        return new_board_state

    def random_alg(self):
        choices = [x for x in range(1, 8) if self.board.cell_not_empty(self.my_position, x)]
        print('MOVE;{}'.format(random.choice(choices)))

    def max_alg(self):
        scores = []

        # Max algorithm - simulate every next possible move and do the one that gives us most pebbles
        for i in range(1, 8):
            if self.board.cell_not_empty(self.my_position, i):
                move_result_board, _ = self.board.generate_move(self.my_position, i)

                heappush(scores, (-1 * move_result_board.get_well_score(self.my_position), i))
        score = heappop(scores)[1]

        log('MOVE;{}'.format(score))
        print('MOVE;{}'.format(score))

    def min_max_alg(self, simulation_board, depth, alpha, beta, maximizing_player, side):
        # base case - no moves left
        if simulation_board.no_moves_left(side):
            return simulation_board.get_evaluation(maximizing_player), 0

        # reached maximum depth - heuristics - now random
        if depth == 0:
            choices = [x for x in range(1, 8) if simulation_board.cell_not_empty(side, x)]
            return simulation_board.get_evaluation(maximizing_player), random.choice(choices)

        # apply min max
        if maximizing_player:
            max_evaluation = -math.inf
            max_i = 0
            for i in range(7, 0, -1):
                if simulation_board.cell_not_empty(side, i):
                    child, ended_in_own_well = simulation_board.generate_move(side, i)

                    # One more turn if it ended in it's own well
                    if ended_in_own_well:
                        evaluation, _ = self.min_max_alg(child, depth - 1, alpha, beta, True, side)
                    else:
                        evaluation, _ = self.min_max_alg(child, depth - 1, alpha, beta, False, opposite_side(side))

                    if max_evaluation < evaluation:
                        max_i = i
                        max_evaluation = evaluation

                    alpha = max(alpha, evaluation)

                if beta <= alpha:  # not sure about indentation of this
                    break

            return max_evaluation, max_i

        else:
            min_evaluation = math.inf
            min_i = 0
            for i in range(7, 0, -1):
                if simulation_board.cell_not_empty(side, i):
                    child, ended_in_own_well = simulation_board.generate_move(side, i)

                    # One more turn if it ended in it's own well
                    if self.first_turn:
                        self.first_turn = False
                        evaluation, _ = self.min_max_alg(child, depth - 1, alpha, beta, True, opposite_side(side))
                    else:
                        if ended_in_own_well:
                            evaluation, _ = self.min_max_alg(child, depth - 1, alpha, beta, False, side)
                        else:
                            evaluation, _ = self.min_max_alg(child, depth - 1, alpha, beta, True, opposite_side(side))

                    if min_evaluation > evaluation:
                        min_i = i
                        min_evaluation = evaluation

                    beta = min(beta, evaluation)

                if beta <= alpha:  # not sure about indentation of this
                    break

            return min_evaluation, min_i


game_over = False
board = Board()
agent = Tortellini(board)
is_SWAP_an_option = False
# variable to keep the bord state of how we would move if we were the opponent
# (only used in first turn to decide if we swap)
board_we_would_get_to = None


# TODO: delete stacktrace log
try:
    while not game_over:
        command = input()
        args = command.split(';')
        if args[0] == 'START':
            if args[1] == SOUTH:
                agent.first_turn = True
                agent.my_position, agent.opp_position = SOUTH_SIDE, NORTH_SIDE
                move = agent.make_move(agent.my_position)
                print('MOVE;{}'.format(move))
                log("MOVE :" + str(move))
            elif args[1] == NORTH:
                agent.first_turn = False
                agent.my_position, agent.opp_position = NORTH_SIDE, SOUTH_SIDE
                is_SWAP_an_option = True
            else:
                log("Command not valid")

        elif args[0] == 'END':
            game_over = True

        elif args[0] == 'CHANGE':
            if args[1] == 'SWAP':
                agent.my_position, agent.opp_position = agent.opp_position, agent.my_position
                move = agent.make_move(agent.my_position)
                print('MOVE;{}'.format(move))
                log("MOVE :" + str(move))

            else:
                board.update(args[2])
                if args[3] == 'YOU':
                    if is_SWAP_an_option:
                        is_SWAP_an_option = False
                        agent.my_position, agent.opp_position = agent.opp_position, agent.my_position
                        print('SWAP')
                    else:
                        move = agent.make_move(agent.my_position)
                        print('MOVE;{}'.format(move))
                        log("MOVE :" + str(move))

except Exception as e:
    log(traceback.extract_tb(e.__traceback__))
    log(e)
