# tiny_rl
Tiny Reinforcement Learning - So small it can be run on a Raspberry Pi

## Install
1. Make a virtual environment

    `python3 -m venv venv`
1. Activate the virtual environment

    `source venv/bin/activate`
1. Install requirements

    `pip install -r requirements.txt`

    if you're on a raspberry pi, this is gonna take about 15 minutes, also it'll heat up your pi, so make sure it's well ventilated
1. Test it out
    
    1. Play an environment yourself:

        `python environments/coin_collector/coin_collector.py`
    
    1. Test the random agent in an environment
    
        `python runner.py -env coin_collector -agent random -step 100 -games 3`
