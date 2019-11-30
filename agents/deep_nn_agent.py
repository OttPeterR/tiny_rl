from agents import agent
import numpy as np
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Flatten, Dropout
from keras.optimizers import Adam



def _processInputs(inputs):
    inputs = inputs[0]/512.0 # normalize
    h,w = inputs.shape
    inputs = inputs.reshape((1, h*w)) # flatten
    return tf.convert_to_tensor(inputs, dtype='float32')

def _construct_model(inputs,n_outputs):
    # Model Params
    hidden_layers = 5
    thickness = 64

    inputs = _processInputs(inputs)
    input_len = inputs.shape[1].value

    model = Sequential()
    model.add(Dense(thickness, input_dim=input_len, activation="relu"))
    for _ in range(hidden_layers):
        model.add(Dense(thickness, activation="relu"))
    model.add(Dense(n_outputs))
    model.compile(loss="mse",optimizer=Adam())

    return model

class DeepNNAgent(agent.Agent):
    def __init__(self, actions, sample_state, *, seed=42, tf_sess=None):
        # super(DeepNNAgent).__init__(actions, sample_state)
        self.actions=actions
        self.model = _construct_model(sample_state, actions)
        tf.compat.v1.set_random_seed(seed)
        if tf_sess is None:
            self.tf_sess = tf.compat.v1.Session()
        else:
            self.tf_sess = tf_sess
    
    def getTFSession(self):
        return self.tf_sess
    
    def act(self, state):
        inputs = _processInputs(state)
        action_probability = self.model(inputs)
        return tf.math.argmax(action_probability)


    def learn(self, state, actions, reward, game_over):
        pass

    def checkpoint(self, filename):
        # model.save(filename)
        pass

    def load(self, checkpoint_file):
        # self.model.load(checkpoint_file)
        pass
