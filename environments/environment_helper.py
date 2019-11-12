###
### Environment Constructors
###
def CoinCollectorEnvironment():
    from environments.coin_collector import coin_collector
    return coin_collector.make_game()

def CoinCollectorUI():
    from environments.coin_collector import coin_collector
    return coin_collector.make_ui()

def ShockwaveEnvironment(level):
    from environments.shockwave import shockwave
    return shockwave.make_game(level)

###
### Convenience Environment Constructors
###

env_dict = {
    "coin_collector":(CoinCollectorEnvironment, 4),
    "shockwave":(ShockwaveEnvironment, 4),
}
ui_dict = {
    "coin_collector":CoinCollectorUI,
}

def environmentList():
    return [x for x in env_dict.keys()]

def uiList():
    return [x for x in ui_dict.keys()]

def getEnvironment(name):
    if name not in env_dict:
        raise(f"{name} not available. Valid choices: {env_dict.keys()}")
        return None
    return env_dict[name][0](), env_dict[name][1]

def getEnvironment(name):
    if name not in ui_dict:
        raise(f"{name} not available. Valid choices: {ui_dict.keys()}")
        return None
    return ui_dict[name]()

