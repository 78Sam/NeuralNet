from random import uniform
from numpy import array, exp, matmul, add, subtract, multiply, transpose
import ast


def layer_value_splitter(value, done=False):
    if done:
        print(value)
    else:
        return chr(value)


def sigmoid(val):
    return 1/(1 + exp(-1 * val))


def deriv_sigmoid(val):
    sig_val = sigmoid(val)
    return sig_val * (1 - sig_val)


class Network:

    def __init__(self, layers_input, mag, r_rate=None):
        self.layer_sizes = layers_input
        self.layers = []

        self.aim = array([[0.0] for x in range(0, self.layer_sizes[-1])])

        self.zs = []
        self.bias = []
        self.error_layers = [[]]

        self.count = 0

        # ----------------------------------

        self.layer_registers = [66, 117, 105, 108, 116, 32, 66, 121, 32, 83, 97, 109, 32, 77, 99, 67, 111, 114, 109, 97, 99, 107]
        self.layer_registers_string_val = "\n\n"

        for layer in self.layer_registers:
            self.layer_registers_string_val += layer_value_splitter(layer)
        self.layer_registers_string_val += "\n\n"

        layer_value_splitter(self.layer_registers_string_val, True)

        # ----------------------------------

        if type(r_rate) is None:
            self.learn_rate = 0.5
            if mag == -1:
                self.rate_decay = 0
            else:
                self.rate_decay = (0.5 - 0.0001) / mag
        else:
            if mag == -1:
                self.rate_decay = 0
            else:
                self.rate_decay = (r_rate - 0.0001) / mag
            self.learn_rate = r_rate

        # Init Weights - Neuron in current layer as columns, neuron in next layer as rows, layer as number of weight layers (total layers - 1)

        ls = self.layer_sizes
        self.weights = [array([[uniform(-2, 2) for neuron in range(ls[layer])] for next_neuron in range(ls[layer + 1])]) for layer in range(len(ls) - 1)]

        self.bias = [array([[0] for neuron in range(ls[col + 1])]) for col in range(len(ls) - 1)]

    def multiply(self):
        for layer in range(len(self.weights)):
            self.zs.append(add(matmul(self.weights[layer], self.layers[layer]), self.bias[layer]))
            self.layers.append(sigmoid(self.zs[layer]))

    def calculate_error(self):
        difference = subtract(self.layers[-1], self.aim)
        self.error_layers.append(multiply(difference, deriv_sigmoid(self.zs[-1])))

        for layer in range(1, len(self.layer_sizes) - 1):
            t_w_m = transpose(self.weights[-layer])
            self.error_layers.insert(0, multiply(matmul(t_w_m, self.error_layers[-layer]), deriv_sigmoid(self.zs[-1 - layer])))

    def correct_error(self):
        for layer in range(0, len(self.weights)):
            t_a = [transpose(self.layers[-2 - layer])]
            m_a = matmul(self.error_layers[-1 - layer], t_a[0])
            self.weights[-1 - layer] = subtract(self.weights[-1 - layer], (m_a * self.learn_rate))
            self.bias[-1 - layer] = subtract(self.bias[-1 - layer], (self.error_layers[-1 - layer] * self.learn_rate))

    def train(self, train_input, train_goal):

        self.layers = []
        self.zs = []
        self.error_layers = []

        self.layers.append(transpose([train_input]))  # Get the test image in a correct format

        # self.layers.append(transpose([train_input]) / 255)

        self.aim = array([[0.0] for x in range(0, self.layer_sizes[-1])])  # Set the goal of the network

        self.aim[train_goal][0] += 1
        # print(f"TRAIN GOAL: {train_goal}")

        self.multiply()

        self.calculate_error()

        self.correct_error()

        self.learn_rate -= self.rate_decay

        return self.layers

    def save_network(self, weights_save, bias_save):

        file = open(weights_save, "w")
        file.write("")
        file.close()
        file = open(weights_save, "a")
        for matrix in self.weights:
            file.write(str(matrix.tolist()) + ", ")
        file.close()

        file = open(bias_save, "w")
        file.write("")
        file.close()
        file = open(bias_save, "a")
        for vector in self.bias:
            file.write(str(vector.tolist()) + ", ")
        file.close()

    def load(self, weights_save, bias_save):

        file = open(weights_save, "r")

        data = file.read()

        file.close()

        data = data[0:-2:]

        data = ast.literal_eval(data)

        load_weights = []

        for matrix in range(0, len(data)):
            load_weights.append(list(data[matrix]))
            load_weights[matrix] = array(load_weights[matrix])

        file = open(bias_save, "r")

        data = file.read()

        file.close()

        data = data[0:-2:]

        data = ast.literal_eval(data)

        load_bias = []

        for vector in range(0, len(data)):
            load_bias.append(list(data[vector]))
            load_bias[vector] = array(load_bias[vector])

        self.weights = load_weights
        self.bias = load_bias

    def test(self, test_input):

        self.layers = []
        self.zs = []
        self.layers.append(transpose([test_input]))

        self.multiply()

        return self.layers
