from environments.coin_collector import coin_collector
from environments.shockwave import shockwave

def CoinCollectorEnvironment():
    return coin_collector.make_game()

def ShockwaveEnvironment(level):
    return shockwave.make_game(level)