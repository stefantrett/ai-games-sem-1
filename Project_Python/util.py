POSITION_SOUTH = 'South'
POSITION_NORTH = 'North'

log_file = open("log.txt", "w")


def log(some_string):
    log_file.write(some_string + '\n')
