NORTH = 'North'
SOUTH = 'South'

NORTH_SIDE = 0
SOUTH_SIDE = 1

DEPTH = 10

log_file = open("log.txt", "w")

# Heuristic 1 Weight
left_most_pit_score_weight = 0.0
# Heuristic 2 Weight
pits_score_weight = 0.85
# Heuristic 3 Weight
number_of_possible_moves_weight = 0.3
# Heuristic 4 Weight
well_points_weight = 2.0
# Heuristic 5 Weight
right_most_position_weight = 0.6


def log(some_object):
    log_file.write(str(some_object) + '\n')


def opposite_side(my_side):
    return 1 - my_side
