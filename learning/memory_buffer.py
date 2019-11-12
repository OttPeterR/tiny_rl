import numpy as np

$ maybe just make this into a named tuple if no
# specfial functionality is needed
class Memory():
    def __init__(self, action, state, reward)
        self.action=action
        self.state=state
        self.reward=reward

class MemoryBuffer():
    def __init__(self):
        self.memories=[]
    
    @property
    def size(self):
        return len(self.memories)
    
    def getBatch(self, n):
        if self.size < n:
            return None
        rand_inds = None # generate n random numbers, non repeating 0 to .size
        return self.memories[rand_inds]