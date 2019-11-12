import numpy as np

$ maybe just make this into a named tuple if no
# specfial functionality is needed
class Memory():
    def __init__(self, action, state, reward)
        self.action=action
        self.state=state
        self.reward=reward

class MemoryBuffer():
    def __init__(self, env_name):
        self.env_name = env_name
        self.memories=[]
    
    @property
    def size(self):
        return len(self.memories)    
    
    def addMemory(memory):
        self.memories += memory
    
    def getBatch(self, n):
        assert self.size > n, "Not enough memories for requested batch size"
        rand_inds = None # n random ints, non repeating, 0-self.size
        return self.memories[rand_inds]

    def clearMemories(self):
        self.memories=[]