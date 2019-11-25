import random
from util import *


class Tortellini:

    def __init__(self, board):
        self.board = board
        self.my_position = ''
        self.opp_position = ''

    def make_move(self):
        scores = {}

        # Max algorithm - simulate every next possible move and do the one that gives us most pebbles
        for i in range(1, 8):
            if self.board.cell_not_empty(self.my_position, i):
                move_result_board = self.board.generate_move(self.my_position, i)
                scores[i] = move_result_board.get_score_for_side(self.my_position)
        score = max(scores, key=scores.get)
        log('MOVE;{}'.format(score))
        print('MOVE;{}'.format(score))
