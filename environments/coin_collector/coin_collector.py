from pycolab.prefab_parts import sprites as prefab_sprites

LEVEL = [ # 10x10 spaces
        '############',
        '#          #',
        '#          #',
        '#          #',
        '#          #',
        '#          #',
        '#          #',
        '#          #',
        '#          #',
        '#          #',
        '#          #',
        '############']
FG_COLORS = {
        'A':(000,000,000), # player
        '#':(700,700,700), # gray wall
        'c':(650,400,000), # small coin
        'C':(900,500,000) # large coin
    }
BG_COLORS = {
        'A':(200,200,200), # player
        '#':(800,800,800), # gray wall
        'c':(000,000,000), # small coin
        'C':(000,000,000) # large coin
    }

class AgentSprite(prefab_sprites.MazeWalker):
    def __init__(self, corner, position, character):
        super(PlayerSprite, self).__init__(
        corner, position, character, impassable='#.@')

    def update(self, actions, board, layers, backdrop, things, the_plot):
        pass

