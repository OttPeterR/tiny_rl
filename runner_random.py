

# 09.07.2018: 
# Agent code execution capability is now available (for logged in users - just click on upper left links).


import platform
print("Python version: " + platform.python_version())
import numpy as np
import datetime

from environments import environment_helper as env_helper
from agents import agent_helper



game_creator_func = env_helper.CoinCollectorEnvironment
agent = agent_helper.RandomAgent(4)
while True:
  # Let's play with a basic Pycolab Gridworlds game.
  print("Start training Coin Collector game.")
  env = game_creator_func()

  observation, reward, _discount = env.its_showtime()
  total_reward = 0

  while not env.game_over:  
      action = agent.act(observation)

      observation, reward, _discount = env.play(action)

      agent.learn(observation, action, reward, env.game_over)
      total_reward += reward if reward is not None else 0

      # print(f"Action: {action}, Total Reward: {total_reward}")

  #/ while not env.game_over:

  print(f"Total Reward: {total_reward}")
  print("Training finished.")

