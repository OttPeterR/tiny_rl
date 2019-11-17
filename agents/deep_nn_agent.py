from agents import agent
import numpy as np
import tensorflow as tf

def _construct_model(inputs,outputs):
    return None

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
        with self.tf_sess.as_default():
            rand_act = (self.actions+1) * tf.compat.v1.random_uniform(())
            return int(rand_act.eval())

    def learn(self, state, actions, reward, game_over):
        pass

    def checkpoint(self, filename):
        # model.save(filename)
        pass

    def load(self, checkpoint_file):
        # self.model.load(checkpoint_file)
        pass
