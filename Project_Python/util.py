NORTH = 'North'
SOUTH = 'South'

NORTH_SIDE = 0
SOUTH_SIDE = 1

DEPTH = 7

log_file = open("log.txt", "w")

evaluation_hyperparameter = 2.0


def log(some_object):
    log_file.write(str(some_object) + '\n')


def opposite_side(my_side):
    return 1 - my_side
