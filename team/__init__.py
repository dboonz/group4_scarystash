#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pelita.player import SimpleTeam
from .demo_player import DrunkPlayer
from .memoryPlayer import MemoryPlayer
from .utils.helper import CollectiveMemory

# (please use relative imports inside your module)

# The default factory method, which this module must export.
# It must return an instance of `SimpleTeam`  containing
# the name of the team and the respective instances for
# the first and second player.

def factory():

    bot1 = MemoryPlayer(is_sender=True)
    bot2 = MemoryPlayer(is_sender=False)
    print('Creating bots {b1} and {b2}'.format(b1 = bot1.__repr__, b2 = bot2.__repr__))
    m = CollectiveMemory(bot1, bot2)
    return SimpleTeam("group4", bot1, bot2)

# For testing purposes, one may use alternate factory methods::
#
#     def alternate_factory():
#          return SimpleTeam("Our alternate Team", AlternatePlayer(), AlternatePlayer())
#
# To be used as follows::
#
#     $ ./pelitagame path_to/groupN/:alternate_factory

