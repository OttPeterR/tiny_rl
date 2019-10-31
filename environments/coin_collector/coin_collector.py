import sys
import curses

from pycolab import ascii_art
from pycolab import human_ui
from pycolab import things as plab_things
from pycolab.prefab_parts import sprites as prefab_sprites

LEVEL = [ # 10x10 spaces
        '############',
        '#          #',
        '#          #',
        '#          #',
        '#          #',
        '#    A     #',
        '#          #',
        '#          #',
        '#          #',
        '#          #',
        '#          #',
        '############']
FG_COLORS = {
        'A':(000,000,000), # player
        '#':(700,700,700), # gray wall
        'C':(650,400,000), # coin
    }
BG_COLORS = {
        'A':(200,200,200), # player
        '#':(800,800,800), # gray wall
        'C':(000,000,000), # coin
    }

class AgentSprite(prefab_sprites.MazeWalker):
    def __init__(self, corner, position, character):
        super(AgentSprite, self).__init__(
        corner, position, character, impassable='#.@')

    def update(self, actions, board, layers, backdrop, things, the_plot):
        # basic movement
        if actions == 0:  # go upward?
            self._north(board, the_plot)
            the_plot.add_reward(-1)
        elif actions == 1:  # go downward?
            self._south(board, the_plot)
            the_plot.add_reward(-1)
        elif actions == 2:  # go leftward?
            self._west(board, the_plot)
            the_plot.add_reward(-1)
        elif actions == 3:  # go rightward?
            self._east(board, the_plot)
            the_plot.add_reward(-1)
        elif actions == 9:  # quit?
            the_plot.terminate_episode()
        
        # collect a coin
        if 'C' in layers and layers['C'][self.position]:
            the_plot.add_reward(15)
            the_plot.terminate_episode()

class CoinHandler(plab_things.Drape):
    def __init__(self, curtain, character):
        super(CoinHandler, self).__init__(curtain, character)
        self._coins = []
        self._remaining_coins = 10

    def update(self, actions, board, layers, backdrop, things, the_plot):
        # need to add a coin
        if len(self._coins) == 0:
            # player just got the last coin
            if self._remaining_coins == 0:
                the_plot.terminate_episode()
            
            # place coin randomly where there is no player
            self._remaining_coins -= 1
            #TODO




def make_game():
  return ascii_art.ascii_art_to_game(
      art=LEVEL,
      what_lies_beneath=' ',
      sprites={'A': AgentSprite},
      drapes={},
      update_schedule=[['A']],  # Move player
      z_order=['A'])  # Draw 

def main(argv=()):
  game = make_game()

  ui = human_ui.CursesUi(
      keys_to_actions={
          # Basic movement.
          curses.KEY_UP: 0,
          curses.KEY_DOWN: 1,
          curses.KEY_LEFT: 2,
          curses.KEY_RIGHT: 3,
          -1: 4,  # Do nothing.
          'q': 9,
          'Q': 9,
      },
      delay=50,
      colour_fg=FG_COLORS,
      colour_bg=BG_COLORS)

  ui.play(game)


if __name__ == '__main__':
  main(sys.argv)
