
###
### Agent Constructors
###
def RandomAgent():
    from agents import random_agent
    return random_agent.RandomAgent

def DeepNNAgent():
    from agents import deep_nn_agent
    return deep_nn_agent.DeepNNAgent

def RainbowAgent():
    from agents import rainbow
    return rainbow.RainbowAgent
    
def A3CAgent():
    from agents import a3c
    return a3c.A3CAgent

###
### Convenience Agent Constructors
###
agent_dict = {
    "random":RandomAgent,
    "deep_nn":DeepNNAgent,
    "rainbow":RainbowAgent,
    "a3c":A3CAgent,
}

def agentList():
    return [x for x in agent_dict.keys()]

def getAgent(name):
    if name not in agent_dict:
        raise(f"{name} not available. Valid choices: {agent_dict.keys()}")
        return None
    return agent_dict[name]()
