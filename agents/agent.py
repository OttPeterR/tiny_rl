import abc
import six

@six.add_metaclass(abc.ABCMeta)
class Agent():

    @abc.abstractmethod
    def act(self, state):
        pass

    @abc.abstractmethod
    def learn(self, state, action, reward, game_over):
        pass

    @abc.abstractmethod
    def checkpoint(self, filename):
        pass

    @abc.abstractmethod
    def load(self, checkpoint_file):
        pass
