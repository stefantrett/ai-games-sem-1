NORTH = 'North'
SOUTH = 'South'

NORTH_SIDE = 0
SOUTH_SIDE = 1

DEPTH = 10

log_file = open("log.txt", "w")


def log(some_string):
    log_file.write(str(some_string) + '\n')


def opposite_side(my_side):
    return 1 - my_side
