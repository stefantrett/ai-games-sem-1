import random


class Tortellini:

    def __init__(self, board):
        self.board = board
        self.my_position = ''
        self.opp_position = ''

    def not_empty(self, x):
        if self.my_position == 'South':
            return self.board.south[x] != 0
        else:
            return self.board.north[x] != 0

    def make_move(self):
        choices = [x for x in range(1, 8) if self.not_empty(x)]
        print('MOVE;{}'.format(random.choice(choices)))
