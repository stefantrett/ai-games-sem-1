import random


class Tortellini:

    def __init__(self, board):
        self.board = board

    def make_move(self):
        print('MOVE;{}'.format(random.choice(range(1, 7))))
