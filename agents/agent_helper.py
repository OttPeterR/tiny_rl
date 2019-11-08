
###
### Agent Constructors
###
def RandomAgent():
    from agents import random_agent
    return random_agent.RandomAgent

def DeepNNAgent():
    from agents import deep_nn_agent
    return deep_nn_agent.DeepNNAgent


###
### Convenience Agent Constructors
###
agent_dict = {
    "random":RandomAgent,
    "deep_nn":DeepNNAgent,
}

def agentList():
    return [x for x in agent_dict.keys()]

def getAgent(name):
    if name not in agent_dict:
        raise(f"{name} not available. Valid choices: {agent_dict.keys()}")
        return None
    return agent_dict[name]()