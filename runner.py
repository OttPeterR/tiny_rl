import logging
import time
import argparse
import platform
import numpy as np

### tiny_rl packages
from environments import environment_helper as env_helper
from agents import agent_helper

### some system info
logging.basicConfig(level=logging.INFO, \
    format='LOG:%(levelname)s  %(message)s')
logging.info("Python version: " + platform.python_version())

### argparse
my_parser = argparse.ArgumentParser(description='Train an Agent in an Envirnoment',
                                    add_help=True)
my_parser.add_argument('-agent', type=str, required=True,
                       help=f'The Agent to use: {agent_helper.agentList()}')
my_parser.add_argument('-env', type=str, required=True,
                       help=f'The Environment to use: {env_helper.environmentList()}')
args = my_parser.parse_args()


### create everything
logging.info("Creating environment and agent")
render = False
frames_per_second = 5
game_creator_func = env_helper.CoinCollectorEnvironment
agent = agent_helper.getAgent('random')(4)
ui = env_helper.CoinCollectorUI()


### Run it
logging.info("Beginning Training...")
time_training_start = time.time()
while True:
    # Let's play with a basic Pycolab Gridworlds game.
    logging.info("Start New Game.")
    time_round_start = time.time()
    env = game_creator_func()

    observation, reward, _discount = env.its_showtime()
    total_reward = 0
    total_steps = 0

    time_action_sum = 0
    time_learn_sum = 0
    time_step_sum = 0

    while not env.game_over:
        time_step_start = time.time()
        total_steps += 1

        # Act
        time_before_action = time.time()  
        action = agent.act(observation)
        action_duration = time.time() - time_before_action
        time_action_sum += action_duration

        # Simulate one Time Step
        observation, reward, _discount = env.play(action)
        total_reward += reward if reward is not None else 0

        # Learn
        time_before_learn = time.time()
        agent.learn(observation, action, reward, env.game_over)
        learn_duration = time.time() - time_before_learn
        time_learn_sum += learn_duration

        # DRaw to the screen
        if render:
            time.sleep(1.0/frames_per_second)
            # ??? UI.render ???
    #/ round complete

    round_duration = time.time() - time_round_start
    avg_time_per_actions = time_action_sum/total_steps
    avg_time_per_learn = time_learn_sum/total_steps
    avg_time_per_step = time_step_sum/total_steps

    logging.info(f"  Total Reward: {total_reward:0.1f}")
    logging.info(f"  Avg. Seconds/Action: {avg_time_per_actions:0.4f} ")
    logging.info(f"  Avg. Seconds/Learn: {avg_time_per_learn:0.4f} ")
    logging.info(f"  Avg. Seconds/Step:  {avg_time_per_step:0.4f} ")
    logging.info(f"  Round Time (Seconds): {round_duration:0.2f}")

