from agents import agent
import random
import numpy as np
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Flatten, Dropout
from keras.optimizers import Adam
from tqdm import tqdm




def _processInputs(inputs):
    inputs = inputs[0]/512.0 # normalize
    h,w = inputs.shape
    inputs = inputs.reshape(h*w) # flatten
    return np.array([inputs])


class DeepNNAgent(agent.Agent):
    def __init__(self, actions, sample_state, *, tf_sess=None):
        # super(DeepNNAgent).__init__(actions, sample_state)
        self.actions=actions
        self.memory = []
        self.memory_limit = 64_000
        self.random_move_chance=0.05
        if tf_sess is None:
            self.tf_sess = tf.compat.v1.Session()
        else:
            self.tf_sess = tf_sess
        tf.compat.v1.set_random_seed(42)


        # Model 
        hidden_layers = 5
        thickness = 64
        inputs = _processInputs(sample_state)
        input_len = inputs.size
        self.model = Sequential()
        self.model.add(Dense(thickness, input_dim=input_len, activation="relu"))
        for _ in range(hidden_layers):
            self.model.add(Dense(thickness, activation="relu"))
        self.model.add(Dense(actions, activation="sigmoid"))
        self.model.compile(loss="mse",optimizer=Adam())

        
    
    def getTFSession(self):
        return self.tf_sess
    
    def act(self, state):
        # roll dice to do a random move
        if np.random.random() < self.random_move_chance:
            return np.random.randint(self.actions)
        inputs = np.array(_processInputs(state))
        action_probability = self.model.predict(inputs)
        move = np.argmax(action_probability)
        return move



    def saveStateTransition(self, old_state, new_state, action, reward, game_over):
        self.memory.append((old_state, new_state, action, reward, game_over))
        while len(self.memory) > self.memory_limit:
            rand_index = np.random.randint(self.memory_limit)
            del self.memory[rand_index]

    def learn(self):
        batch_size = 512
        epochs = 10

        if len(self.memory) < batch_size: 
            return
        prog_bar = tqdm(total=batch_size*epochs, desc=f"Learning (Epoch: 1 of {epochs})")
        for epoch in range(epochs):
            samples = random.sample(self.memory, batch_size)
            for sample in samples:
                prog_bar.update(1)
                prog_bar.set_description(f"Learning (Epoch: {epoch+1} of {epochs})")
                s_old_state, s_new_state, s_action, s_reward, s_game_over = sample
                target_action = [0]*self.actions
                target_action[s_action] = 1
                inputs = _processInputs(s_old_state)
                self.model.fit([inputs], [[target_action]], epochs=1, verbose=0)   


    def checkpoint(self, filename):
        filename=filename+".ckpt"
        self.model.save_weights(filename)
        return filename

    def load(self, checkpoint_file):
        self.model.load_weights(checkpoint_file)
        pass
