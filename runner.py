import logging
import time
import argparse
import platform
import numpy as np
from tqdm import tqdm

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
my_parser.add_argument('-steps', type=int, default=-1, help="Total steps per round before ending, 0 for unlimited steps")
my_parser.add_argument('-games', type=int, default=-1, help="Total number of games to play, 0 for unlimited")
my_parser.add_argument('-checkpoint', type=str, default=None, help="Name of checkpoint file located in ./agents/checkpoints/")
args = my_parser.parse_args()


### create everything
logging.info(f"Creating...")
render = True if args.fps > 0 else False
frames_per_second = args.fps
frame_time = 1.0/frames_per_second
max_steps = args.steps if args.steps>0 else -1
max_games = args.games if args.games>0 else -1

logging.info(f"Env:   {args.env}")
game_creator_func, actions = env_helper.getEnvironment(args.env)
env = game_creator_func()
observation, _, _ = env.its_showtime()
ui = env_helper.getEnvironment(args.env)

logging.info(f"Agent: {args.agent}")
agent = agent_helper.getAgent(args.agent)(actions, observation)
checkpoint = args.checkpoint
if checkpoint is not None:
    agent.load(f"./agents/checkpoints/{args.checkpoint}")
    logging.info(f"Checkpoint Loaded")
    
logging.info("Setup Complete\n")



### Run it
logging.info("Beginning Training...")
time_training_start = time.time()

total_games=0
while max_games==-1 or total_games<max_games:
    total_games+=1
    logging.info(f"[Game {total_games}]")
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

    prog_bar = tqdm(total=max_steps if max_steps>0 else 10_000)
    prog_bar.update(0)
    while (not env.game_over) and (max_steps==-1 or total_steps<max_steps):
        time_step_start = time.time()
        total_steps += 1
        prog_bar.update(1)

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
            #TODO UI.render 
    round_duration = time.time() - time_round_start
    avg_time_per_actions = time_action_sum/total_steps
    avg_time_per_learn = time_learn_sum/total_steps
    avg_time_per_step = time_step_sum/total_steps

    ### Print out final metrics after one round
    prog_bar.close()
    if not env.game_over:
        logging.info(f"Game Maxed-Out Step Limit, No Victory")
    logging.info(f"Total Reward: {total_reward:0.1f}")
    logging.info(f"Avg. Seconds/Action: {avg_time_per_actions:0.4f} ")
    logging.info(f"Avg. Seconds/Learn: {avg_time_per_learn:0.4f} ")
    logging.info(f"Avg. Seconds/Step:  {avg_time_per_step:0.4f} (Excludes rendering)")
    logging.info(f"Total Steps: {total_steps}")
    logging.info(f"Round Time (Seconds): {round_duration:0.2f}")    
    checkpoint_file = f"./agents/checkpoints/{args.agent}-round_{total_games}"
    checkpoint_file = agent.checkpoint(checkpoint_file)
    logging.info(f"Checkpoint saved to: {checkpoint_file}")
    logging.info("Round Complete\n")

logging.info("Training Complete.")
