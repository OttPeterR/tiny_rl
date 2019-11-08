from agents import random_agent, deep_nn_agent

###
### Agent Constructors
###
def RandomAgent(actions):
    return random_agent.RandomAgent(actions)

def DeepNNAgent(actions, inputs):
    return deep_nn_agent.DeepNNAgent(actions, inputs)


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
    return agent_dict[name]