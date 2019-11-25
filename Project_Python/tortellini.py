import random
from util import *


class Tortellini:

    def __init__(self, board):
        self.board = board
        self.my_position = ''
        self.opp_position = ''

    def make_move(self):
        choices = [x for x in range(1, 8) if self.board.cell_not_empty(self.my_position, x)]
        print('MOVE;{}'.format(random.choice(choices)))
