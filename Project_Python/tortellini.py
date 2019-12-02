import math
import random
from copy import deepcopy
from heapq import heappop, heappush

from util import *


class Tortellini:

    def __init__(self, board):
        self.board = board
        self.my_position = SOUTH_SIDE
        self.opp_position = NORTH_SIDE

    # TODO: why not use self.my_position instead of SOUTH_SIDE?
    def make_move(self):
        print('MOVE;{}'.format(self.min_max_alg(deepcopy(self.board), DEPTH, False, SOUTH_SIDE, 0)[1]))

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

    def min_max_alg(self, board, depth, maximizing_player, side, index):
        if depth == 0 or board.no_moves_left(side):
            return board.get_evaluation(), index

        if maximizing_player:
            max_evaluation = -math.inf
            max_i = 0
            for i in range(1, 8):
                if self.board.cell_not_empty(side, i):
                    child, ended_in_opposite_side = self.board.generate_move(side, i)

                    # One more turn if it ended in the opposite side
                    if ended_in_opposite_side:
                        evaluation, _ = self.min_max_alg(child, depth - 1, True, side, i)
                    else:
                        evaluation, _ = self.min_max_alg(child, depth - 1, False, opposite_side(side), i)

                    if max_evaluation < evaluation:
                        max_i = i
                        max_evaluation = evaluation

            return max_evaluation, max_i

        else:
            min_evaluation = math.inf
            min_i = 0
            for i in range(1, 8):
                if self.board.cell_not_empty(side, i):
                    child, ended_in_opposite_side = self.board.generate_move(side, i)

                    # One more turn if it ended in the opposite side
                    if ended_in_opposite_side:
                        evaluation, _ = self.min_max_alg(child, depth - 1, False, side, i)
                    else:
                        evaluation, _ = self.min_max_alg(child, depth - 1, True, opposite_side(side), i)

                    if min_evaluation > evaluation:
                        min_i = i
                        min_evaluation = evaluation

            return min_evaluation, min_i
