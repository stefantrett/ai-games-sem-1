import math
import random
from heapq import heappop, heappush

from util import *


class Tortellini:

    def __init__(self, board):
        self.board = board
        self.my_position = ''
        self.opp_position = ''

    def make_move(self):
        self.min_max_alg()

    def random(self):
        choices = [x for x in range(1, 8) if self.board.cell_not_empty(self.my_position, x)]
        print('MOVE;{}'.format(random.choice(choices)))

    def max_alg(self):
        scores = []

        # Max algorithm - simulate every next possible move and do the one that gives us most pebbles
        for i in range(1, 8):
            if self.board.cell_not_empty(self.my_position, i):
                move_result_board = self.board.generate_move(self.my_position, i)

                heappush(scores, (-1 * move_result_board.get_score_for_side(self.my_position), i))
        score = heappop(scores)[1]

        log('MOVE;{}'.format(score))
        print('MOVE;{}'.format(score))

    def min_max_alg(self, board, depth, maximizing_player, side):
        if depth == 0 or board.check_game_over(side):
            return board.get_evaluation(), 0

        if maximizing_player:
            max_evaluation = -math.inf
            max_i = 0
            for i in range(1, 8):
                if self.board.cell_not_empty(side, i):
                    child = self.board.generate_move(side, i)
                    evaluation, last_move = self.min_max_alg(child, depth - 1, False, opposite_side(side))
                    if max_evaluation < evaluation:
                        max_i = i
                        max_evaluation = evaluation

            return max_evaluation, max_i

        else:
            min_evaluation = math.inf

            for i in range(1, 8):
                if self.board.cell_not_empty(side, i):
                    child = self.board.generate_move(side, i)
                    evaluation = self.min_max_alg(child, depth - 1, True, opposite_side(side))
                    min_evaluation = min(min_evaluation, evaluation)

            return min_evaluation
