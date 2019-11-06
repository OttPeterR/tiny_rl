from agents import agent
import numpy as np

class RandomAgent(agent.Agent):
    def __init__(self, actions):
        super(RandomAgent).__init__()
        self.actions=actions

    def act(self, state):
        return np.random.choice(self.actions+1)

    def learn(self, state, action, reward, game_over):
        pass

    def checkpoint(self, filename):
        pass

    def load(self, checkpoint_file):
        pass
