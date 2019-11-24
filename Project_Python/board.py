class Board:

    def __init__(self):
        self.north = [7, 7, 7, 7, 7, 7, 7, 0]
        self.south = [7, 7, 7, 7, 7, 7, 7, 0]
        self.log_file = open("board_log.txt", "w")

    def update(self, board_state):
        positions = board_state.split(',')
        self.north = positions[:8]
        self.south = positions[8:]

    def print_board(self):
        self.log_file.write(str(self.north[7]) + " -- " + str(self.north[:7:-1]))
        self.log_file.write(str(self.south[:7]) + " -- " + str(self.south[7]))
