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
my_parser.add_argument('-agent', type=str, default="random",
                       help=f'The Agent to use: {agent_helper.agentList()}')
my_parser.add_argument('-env', type=str, default="coin_collector",
                       help=f'The Environment to use: {env_helper.environmentList()}')
my_parser.add_argument('-fps', type=int, default=-1, help='Frames per Second')
args = my_parser.parse_args()


### create everything
logging.info(f"Creating...")
logging.info(f"Agent: {args.agent}")
logging.info(f"Env:   {args.env}")
render = True if args.fps > 0 else False
frames_per_second = args.fps
frame_time = 1.0/frames_per_second
game_creator_func = env_helper.CoinCollectorEnvironment
env = game_creator_func()
observation, _, _ = env.its_showtime()
#FIXME env.get_actions = 4
actions = 4
agent = agent_helper.getAgent(args.agent)(actions, observation)
ui = env_helper.getEnvironment(args.env)
logging.info("Setup Complete\n")

### Run it
logging.info("Beginning Training...")
time_training_start = time.time()
while True:
    logging.info("Starting New Game...")
    time_round_start = time.time()
    env = game_creator_func()

    ### Start environment
    observation, reward, _discount = env.its_showtime()
    
    ### Init timers and counters
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
        time_action_sum += time.time() - time_before_action

        # Simulate one Time Step
        observation, reward, _discount = env.play(action)
        total_reward += reward if reward is not None else 0

        # Learn
        time_before_learn = time.time()
        agent.learn(observation, action, reward, env.game_over)
        time_learn_sum += time.time() - time_before_learn

        time_step_duration = time.time() - time_step_start
        time_step_sum += time_step_duration
        
        # Draw to the screen
        if render:
            time_diff = frame_time - time_step_duration
            if time_diff>0:
                time.sleep(time_diff)
            #FIXME ??? UI.render ???

    round_duration = time.time() - time_round_start
    avg_time_per_actions = time_action_sum/total_steps
    avg_time_per_learn = time_learn_sum/total_steps
    avg_time_per_step = time_step_sum/total_steps

    ### Print out final metrics after one round
    logging.info(f"Total Reward: {total_reward:0.1f}")
    logging.info(f"Avg. Seconds/Action: {avg_time_per_actions:0.4f} ")
    logging.info(f"Avg. Seconds/Learn: {avg_time_per_learn:0.4f} ")
    logging.info(f"Avg. Seconds/Step:  {avg_time_per_step:0.4f} (Excludes rendering)")
    logging.info(f"Round Time (Seconds): {round_duration:0.2f}")
    logging.info("Round Complete\n")

loggin.info("Training Complete.")