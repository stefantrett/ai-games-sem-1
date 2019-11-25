import random
from util import *
from heapq import heappop, heappush

class Tortellini:

    def __init__(self, board):
        self.board = board
        self.my_position = ''
        self.opp_position = ''

    def random(self):
        choices = [x for x in range(1, 8) if self.board.cell_not_empty(self.my_position, x)]
        print('MOVE;{}'.format(random.choice(choices)))

    def make_move(self):
        scores = []

        # Max algorithm - simulate every next possible move and do the one that gives us most pebbles
        for i in range(1, 8):
            if self.board.cell_not_empty(self.my_position, i):
                log(i)
                move_result_board = self.board.generate_move(self.my_position, i)
                heappush(scores, (-1 * move_result_board.get_score_for_side(self.my_position), i))
        score = heappop(scores)[1]
        log(score)
        log('MOVE;{}'.format(score))
        print('MOVE;{}'.format(score))
