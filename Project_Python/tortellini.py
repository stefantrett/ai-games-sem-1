import math
import random
from copy import deepcopy
from heapq import heappop, heappush

from board import Board
from util import *


class Tortellini:

    def __init__(self, board):
        self.board = board
        self.my_position = SOUTH_SIDE
        self.opp_position = NORTH_SIDE

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

        move = self.min_max_alg(Board(), DEPTH, -math.inf, math.inf, maximizing, side)[1]
        new_board_state, _ = Board().generate_move(side, move)
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
            return simulation_board.get_evaluation(), 0

        # reached maximum depth - heuristics - now random
        if depth == 0:
            choices = [x for x in range(1, 8) if simulation_board.cell_not_empty(side, x)]
            return simulation_board.get_evaluation(), random.choice(choices)

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
