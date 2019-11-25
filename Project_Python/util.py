POSITION_SOUTH = 'South'
POSITION_NORTH = 'North'

DEPTH = 10

log_file = open("log.txt", "w")


def log(some_string):
    log_file.write(str(some_string) + '\n')


def opposite_side(side):
    if side == POSITION_SOUTH:
        return POSITION_NORTH
    else:
        return POSITION_SOUTH
