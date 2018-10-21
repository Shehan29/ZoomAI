import numpy as np
import pyautogui
import sys
from GameUtils import initialize_objects


def sigmoid(x):
    return 1.0/(1.0 + np.exp(-x))


def relu(vector):
    vector[vector < 0] = 0
    return vector


def apply_neural_nets(weights, observation_matrix):
    """ Based on the observation_matrix and weights, compute the new hidden layer values
    and the new output layer values"""
    hidden_layer_values = np.dot(weights['1'], observation_matrix)
    hidden_layer_values = relu(hidden_layer_values)
    output_layer_values = np.dot(hidden_layer_values, weights['2'])
    output_layer_values = sigmoid(output_layer_values)
    return hidden_layer_values, output_layer_values


def discount_rewards(rewards, gamma):
    """ Actions you took 20 steps before the end result are less important to the overall result than an action you took a step ago.
    This implements that logic by discounting the reward on previous actions based on how long ago they were taken"""
    discounted_rewards = np.zeros_like(rewards)
    running_add = 0
    for t in reversed(range(0, rewards.size)):
        running_add = running_add * gamma + rewards[t]
        discounted_rewards[t] = running_add
    return discounted_rewards


def discount_with_rewards(gradient_log_p, episode_rewards, gamma):
    """ discount the gradient with the normalized rewards """
    discounted_episode_rewards = discount_rewards(episode_rewards, gamma)
    # standardize the rewards to be unit normal (helps control the gradient estimator variance)
    discounted_episode_rewards = np.subtract(discounted_episode_rewards, np.mean(discounted_episode_rewards))
    discounted_episode_rewards /= np.std(discounted_episode_rewards)
    return gradient_log_p * discounted_episode_rewards


ACTIONS = {0: "LEFT", 1: "STAY", 2: "RIGHT"}


def choose_action(probability):
    print(probability)
    if np.random.uniform() < probability:
        return 0
    else:
        return 2


class NeuralNetwork:
    def __init__(self):
        self.batch_size = 20  # how many episodes to wait before moving the weights
        self.gamma = 0.99  # discount factor for reward
        self.decay_rate = 0.99
        self.num_hidden_layer_neurons = 50  # number of neurons
        self.input_dimensions = 2  # dimension of our observation images
        self.learning_rate = 1e-4
        self.weights = {
          '1': np.random.randn(self.num_hidden_layer_neurons, self.input_dimensions) / np.sqrt(self.input_dimensions),
          '2': np.random.randn(self.num_hidden_layer_neurons) / np.sqrt(self.num_hidden_layer_neurons)
        }

        # To be used with rmsprop algorithm (http://sebastianruder.com/optimizing-gradient-descent/index.html#rmsprop)
        self.expectation_g_squared = {}
        self.g_dict = {}
        for layer_name in self.weights.keys():
            self.expectation_g_squared[layer_name] = np.zeros_like(self.weights[layer_name])
            self.g_dict[layer_name] = np.zeros_like(self.weights[layer_name])

    def compute_gradient(self, gradient_log_p, hidden_layer_values, observation_values):
        """ See here: http://neuralnetworksanddeeplearning.com/chap2.html"""
        delta_L = gradient_log_p[1:]  # exclude first value
        dC_dw2 = np.dot(hidden_layer_values.T, delta_L).ravel()

        delta_l2 = np.outer(delta_L, self.weights['2'])
        delta_l2 = relu(delta_l2)
        dC_dw1 = np.dot(delta_l2.T, observation_values)
        return {
            '1': dC_dw1,
            '2': dC_dw2
        }

    def update_weights(self):
        """ See here: http://sebastianruder.com/optimizing-gradient-descent/index.html#rmsprop"""
        epsilon = 1e-5
        for layer_name in self.weights.keys():
            g = self.g_dict[layer_name]
            self.expectation_g_squared[layer_name] = self.decay_rate * self.expectation_g_squared[layer_name] + (
                                                                                                 1 - self.decay_rate) * g ** 2
            self.weights[layer_name] += (self.learning_rate * g) / (np.sqrt(self.expectation_g_squared[layer_name] + epsilon))
            self.g_dict[layer_name] = np.zeros_like(self.weights[layer_name])  # reset batch gradient buffer

    def train(self, input_pipe):
        episode_hidden_layer_values, episode_observations = [], []
        episode_gradient_log_ps, episode_rewards = [], []
        reward_sum = 0
        running_reward = None
        right_probability = 0.5
        car, obstacle = initialize_objects()  # used to get properties about the objects

        for epoch in range(1, 1000):
            print("Epoch " + str(epoch))
            prev_action = 1  # STAY
            dodged = 0

            # start = time.time()

            while True:
                data = input_pipe.recv()

                pyautogui.keyUp('left')
                pyautogui.keyUp('right')

                if data == "QUIT":
                    sys.exit()

                reward = 5

                if "CRASH" in data:
                    reward = -10
                elif ((data['car_x'] + car.width) > data['obstacle_x']) and (
                    data['car_x'] < (data['obstacle_x'] + obstacle.width)):
                    reward = -8  # about to hit obstacle
                elif data['car_x'] < 200 or data['car_x'] < car.display_width - 200:
                    reward = -5  # discourage going to close to walls
                # elif prev_action == 1:
                #     reward = 5  # encourage not moving if not in danger

                if data["dodged"] > dodged:
                    dodged = data["dodged"]
                    reward = 10


                # evaluate previous action
                reward_sum += reward
                episode_rewards.append(reward)

                fake_label = 1 if prev_action == 2 else 0
                loss_function_gradient = fake_label - right_probability
                episode_gradient_log_ps.append(loss_function_gradient)

                if "CRASH" in data:
                    episode_hidden_layer_values = np.vstack(episode_hidden_layer_values)
                    episode_observations = np.vstack(episode_observations)
                    episode_gradient_log_ps = np.vstack(episode_gradient_log_ps)
                    episode_rewards = np.vstack(episode_rewards)

                    # Tweak the gradient of the log_ps based on the discounted rewards
                    episode_gradient_log_ps_discounted = discount_with_rewards(episode_gradient_log_ps, episode_rewards,
                                                                               self.gamma)
                    gradient = self.compute_gradient(
                        episode_gradient_log_ps_discounted,
                        episode_hidden_layer_values,
                        episode_observations
                    )

                    for layer_name in gradient:
                        self.g_dict[layer_name] += gradient[layer_name]

                    if epoch % self.batch_size == 0:
                        self.update_weights()

                    episode_hidden_layer_values, episode_observations, episode_gradient_log_ps, episode_rewards = [], [], [], []  # reset values
                    running_reward = reward_sum if running_reward is None else running_reward * 0.99 + reward_sum * 0.01

                    # save weights to file
                    np.save('q_table.npy', self.weights)

                    print('resetting env. episode reward total was %f. running mean: %f' % (reward_sum, running_reward))
                    reward_sum = 0
                    break
                else:
                    processed_observations = [data["obstacle_x"], data["car_x"]]

                    hidden_layer_values, right_probability = apply_neural_nets(self.weights, processed_observations)
                    episode_observations.append(processed_observations)
                    episode_hidden_layer_values.append(hidden_layer_values)

                    action = choose_action(right_probability)
                    prev_action = action
                    direction = ACTIONS[action]
                    if direction == "LEFT":
                        pyautogui.keyDown('left')
                    elif direction == "RIGHT":
                        pyautogui.keyDown('right')

