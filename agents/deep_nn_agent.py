from agents import agent
import numpy as np
import tensorflow



def _construct_model(inputs,outputs):
    return None


class DeepNNAgent(agent.Agent):
    def __init__(self, actions, inputs):
        seper(DeepNNAgent).__init__()
        self.actions=actions
        self.model = _construct_model(inputs, actions)


    def act(self, state):
        return np.random.choice(self.actions)

    def learn(self, state, actions, reward, game_over):
        pass

    def checkpoint(self, filename):
        # model.save(filename)
        pass

    def load(self, checkpoint_file):
        # self.model.load(checkpoint_file)
        pass