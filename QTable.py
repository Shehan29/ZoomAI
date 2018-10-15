import numpy as np
import random
from functools import reduce
from GameUtils import initialize_objects

ACTIONS = {0: "STAY", 1: "LEFT", 2: "RIGHT"}


def random_action():
    return random.choice(list(ACTIONS.keys()))


class QTable:
    def __init__(self, q_table, feature_encoding):
        self.q_table = q_table
        self.feature_encoding = feature_encoding


def initialize_q_table():
    car, obstacle = initialize_objects()
    car_space = car.get_binned_space()
    obstacle_space = obstacle.get_binned_space()
    space = {**car_space, **obstacle_space}

    features = list(space.keys())
    feature_encoding = {features[0]: 1}
    prev_feature = features[0]

    for feature in features[:0:-1]:  # skip first feature
        space_value = space[feature]
        feature_encoding[feature] = space_value*feature_encoding[prev_feature]
        prev_feature = feature

    observation_space = reduce((lambda x, y: x * y), feature_encoding.values())

    return np.zeros([observation_space, len(ACTIONS)]), feature_encoding


q_table = QTable(*initialize_q_table())


def encode(data):
    state = 0
    for feature, encoding in q_table.feature_encoding.items():
        state += encoding * data[feature]

    return int(state)
