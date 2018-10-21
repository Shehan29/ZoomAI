import numpy as np
import random
from resources.GameUtils import initialize_traffic

ACTIONS = {0: "LEFT", 1: "STAY", 2: "RIGHT"}


def random_action():
    return random.choice(list(ACTIONS.keys()))


class QTable:
    def __init__(self, table, feature_encoding):
        self.q_table = table
        self.feature_encoding = feature_encoding


def get_space_and_encoding():
    car, obstacle = initialize_traffic()
    car_space = car.get_binned_space()
    obstacle_space = obstacle.get_binned_space()
    space = {**car_space, **obstacle_space}

    features = list(space.keys())
    feature_encoding = {features[0]: 1}
    prev_feature = features[0]
    observation_space = space[features[0]]

    for feature in features[:0:-1]:  # skip first feature
        space_value = space[feature]
        observation_space *= space_value
        feature_encoding[feature] = space[prev_feature]*feature_encoding[prev_feature]
        prev_feature = feature

    return observation_space+1, feature_encoding


def initialize_q_table():
    observation_space, feature_encoding = get_space_and_encoding()
    return np.zeros([observation_space, len(ACTIONS)]), feature_encoding


q_table = QTable(*initialize_q_table())


def encode(data):
    state = 0
    for feature, encoding in q_table.feature_encoding.items():
        state += encoding * data[feature]

    return int(state)
