from agents import agent
import random
import numpy as np
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Flatten, Dropout
from keras.optimizers import Adam
from tqdm import tqdm



def _createModel(input_size, output_actions, learning_rate):
    model = Sequential()
    model.add(Dense(128, input_dim=input_size, activation="relu"))
    model.add(Dense(128, activation="relu"))
    model.add(Dense(128, activation="relu"))
    model.add(Dense(output_actions))
    model.compile(loss="mse", optimizer=Adam(lr=learning_rate))
    return model


def _processInputs(inputs):
    inputs = inputs[0]/512.0 # normalize
    h,w = inputs.shape
    inputs = inputs.reshape(h*w) # flatten
    return np.array([inputs])


class DQNAgent(agent.Agent):
    def __init__(self, actions, sample_state):
        self.actions=actions
        self.memory = []
        self.memory_limit = 512_000

        self.gamma = 0.95 # future reward decay rate
        self.epsilon = 1.0 # exploration/exploitation (1=totally random)
        self.epsilon_min = 0.01 
        self.epsilon_decay = 0.995
        self.learning_rate = 0.01

        inputs = _processInputs(sample_state)
        # this model decides what actions are taken
        self.model = _createModel(inputs.size, actions, self.learning_rate)
        # this model decides which actions *should* be taken
        self.target_model = _createModel(inputs.size, actions, self.learning_rate)    
    
    def act(self, state):
        # roll dice to do a random move
        if np.random.random() < self.epsilon:
            return np.random.randint(self.actions)
        inputs = np.array(_processInputs(state))
        action_probability = self.model.predict(inputs)
        move = np.argmax(action_probability)
        return move



    def saveStateTransition(self, old_state, new_state, action, reward, game_over):
        self.memory.append((old_state, new_state, action, reward, game_over))
        while len(self.memory) > self.memory_limit:
            rand_index = np.random.randint(self.memory_limit*0.05)
            del self.memory[rand_index]
        

    def learn(self):
        self.epsilon *= self.epsilon_decay
        self.epsilon = max(self.epsilon_min, self.epsilon)

        batch_size = 1024
        epochs = min(1+len(self.memory)//batch_size, 25)

        if len(self.memory) < batch_size: 
            return
        prog_bar = tqdm(total=batch_size*epochs, desc=f"Learning (Epoch: 1 of {epochs})")
        for epoch in range(epochs):
            samples = random.sample(self.memory, batch_size)
            for sample in samples:
                prog_bar.update(1)
                prog_bar.set_description(f"Learning (Epoch: {epoch+1} of {epochs})")
                s_old_state, s_new_state, s_action, s_reward, s_game_over = sample
                
                inputs = _processInputs(s_old_state)
                target_action = self.target_model.predict([inputs])[0]
                
                if s_game_over:
                    target_action[s_action] = s_reward
                else:
                    new_inputs = _processInputs(s_new_state)
                    next_actions = self.target_model.predict([new_inputs])[0]
                    Q_future = max(next_actions)
                    target_action[s_action] = s_reward + Q_future * self.gamma
                
                self.model.fit([inputs], [[target_action]], epochs=1, verbose=0)   
        prog_bar.close()
        # copy weights to the target network
        weights = self.model.get_weights()
        target_weights = self.target_model.get_weights()
        for i in range(len(target_weights)):
            target_weights[i] = weights[i]
        self.target_model.set_weights(target_weights)


    def checkpoint(self, filename):
        filename=filename+".ckpt"
        self.model.save_weights(filename)
        return filename

    def load(self, checkpoint_file):
        self.model.load_weights(checkpoint_file)
        self.target_model.load_weights(checkpoint_file)
        pass
