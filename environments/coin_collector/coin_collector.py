import sys
import curses
import random

from pycolab import ascii_art
from pycolab import human_ui
from pycolab import things as plab_things
from pycolab.prefab_parts import sprites as prefab_sprites

LEVEL = [ # 10x10 spaces
        '###########',
        '#         #',
        '#         #',
        '#         #',
        '#         #',
        '#    A    #',
        '#         #',
        '#         #',
        '#         #',
        '#         #',
        '###########']
FG_COLORS = {
        'A':(999,999,999), # player
        '#':(700,700,700), # gray wall
        'C':(850,800,100), # coin
        ' ':(000,000,000), # nothing
    }
BG_COLORS = {
        'A':(200,200,200), # player
        '#':(800,800,800), # gray wall
        'C':(350,300, 50), # coin
        ' ':(000,000,000), # nothing
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
                

class CoinHandler(plab_things.Drape):
    def __init__(self, curtain, character):
        super(CoinHandler, self).__init__(curtain, character)
        self._coins = []
        self._remaining_coins = 20
        self._coins_in_play = 2 # max number of coins on the board
        self._coin_reward = 15

    def update(self, actions, board, layers, backdrop, things, the_plot):
        # game complete
        if self._coins==[] and self._remaining_coins==0:
            the_plot.terminate_episode()
        
        # check if player collects a coin
        for coin in self._coins:
            if 'A' in layers and layers['A'][coin]:
                self.curtain[coin]=False # remove coin
                self._coins.remove(coin)
                the_plot.add_reward(self._coin_reward)

        # need to add a coin
        if len(self._coins) < self._coins_in_play and \
            self._remaining_coins > 0:

            #pick a random location
            random_x = 1+int(random.random()*8) # width
            random_y = 1+int(random.random()*8) # height
            limit = 0
            # check if its already occupied by something
            while layers['C'][random_x,random_y] or \
                  layers['A'][random_x,random_y] or \
                  layers['#'][random_x,random_y]:
                # re-roll if its already occupied
                random_x = 1+int(random.random()*8) # width
                random_y = 1+int(random.random()*8) # height
                # prevent infinite looping
                limit -= -1 # because I'm a chaotic neutral
                if limit > 100:
                    the_plot.log("Could not place coin")

                    break

            # place the coin
            self._coins += [(random_x, random_y)]
            self._remaining_coins -= 1
            self.curtain[random_x, random_y]=True
            the_plot.log(f"Placing coin at ({random_x},{random_y})")


def make_game():
    return ascii_art.ascii_art_to_game(
        art=LEVEL,
        what_lies_beneath=' ',
        sprites={'A': AgentSprite},
        drapes={'C': CoinHandler},
        update_schedule=[['A'],['C']],  # Move player, then update coins
z_order=['C','A'])  # Draw player, then draw coins

def make_ui(*,keys_to_actions={'q': 9,'Q': 9},delay=0.25):
    return human_ui.CursesUi(
                keys_to_actions=keys_to_actions,
                delay=delay,
                colour_fg=FG_COLORS,
                colour_bg=BG_COLORS)

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
            delay=1,
            colour_fg=FG_COLORS,
            colour_bg=BG_COLORS)

    ui.play(game)


if __name__ == '__main__':
  main(sys.argv)
