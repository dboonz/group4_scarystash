#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pelita.player import SimpleTeam
from .role_attacker import ExtremelyHungryRole
from .role_defender import PossessiveItalianRole
from .awesome_player import AwesomePlayer
from .utils.helper import CollectiveMemory
#from .demo_player import DrunkPlayer
#from .memoryPlayer import MemoryPlayer

# (please use relative imports inside your module)

# The default factory method, which this module must export.
# It must return an instance of `SimpleTeam`  containing
# the name of the team and the respective instances for
# the first and second player.

def factory():
    memory = CollectiveMemory()
    bot1 = AwesomePlayer(walkie_talkie=memory, attacker=ExtremelyHungryRole(), defender=ExtremelyHungryRole())
    bot2 = AwesomePlayer(walkie_talkie=memory, attacker=ExtremelyHungryRole(), defender=ExtremelyHungryRole())
#    bot2 = AwesomePlayer(walkie_talkie=memory, attacker=PossessiveItalianRole(), defender=PossessiveItalianRole())
    #
    # bot1 = MemoryPlayer()
    # bot2 = MemoryPlayer()
    # print('Creating bots {b1} and {b2}'.format(b1 = bot1.__repr__, b2 = bot2.__repr__))
    # m = CollectiveMemory(bot1, bot2)
    # bot1 = DrunkPlayer()
    # bot2 = DrunkPlayer()
    return SimpleTeam("popyourstash", bot1, bot2)


def defender_factory():

    memory = CollectiveMemory()
    bot1 = AwesomePlayer(walkie_talkie=memory, attacker=PossessiveItalianRole(), defender=PossessiveItalianRole())
    bot2 = AwesomePlayer(walkie_talkie=memory, attacker=ExtremelyHungryRole(), defender=ExtremelyHungryRole())
#    bot2 = AwesomePlayer(walkie_talkie=memory, attacker=PossessiveItalianRole(), defender=PossessiveItalianRole())
#    bot1 = AwesomePlayer(walkie_talkie=memory, attacker=ExtremelyHungryRole(), defender=ExtremelyHungryRole())
#    bot2 = AwesomePlayer(walkie_talkie=memory, attacker=ExtremelyHungryRole(), defender=ExtremelyHungryRole())
    return SimpleTeam("popyourstash", bot1, bot2)


# For testing purposes, one may use alternate factory methods::
#
#     def alternate_factory():
#          return SimpleTeam("Our alternate Team", AlternatePlayer(), AlternatePlayer())
#
# To be used as follows::
#
#     $ ./pelitagame path_to/groupN/:alternate_factory
