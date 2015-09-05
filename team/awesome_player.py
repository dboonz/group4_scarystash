# -*- coding: utf-8 -*-

# (Specifying utf-8 is always a good idea in Python 2.)


from pelita.player import AbstractPlayer
from pelita.graph import AdjacencyList, NoPathException, diff_pos


class AwesomePlayer(AbstractPlayer):
    '''
    Player which makes awesome move decisions.
    '''
    def __init__(self, attacker, defender, walkie_talkie=None):
        '''
        '''
        self.memory = walkie_talkie
        self.attacker = attacker
        self.defender = defender


    def set_initial(self):
        '''Sets the initial values.
        '''
        self.adjacency = AdjacencyList(self.current_uni.reachable([self.initial_pos]))


    def get_role(self):
        '''Returns the role of the player.
        '''
        if self.memory is None:
            pass
        else:
            pass
        return 'attack'


    def get_move(self):
        '''Returns the next move to be made by the player.
        '''
        # specify the role
        role = self.get_role()
        if role is 'attack':
            self.say(self.attacker.talk)
            move = self.attacker.get_move(player=self)
        elif role is 'defend':
            self.say(self.defender.talk)
            move = self.defender.get_move(player=self)
        else:
            raise ValueError('Donnot know what to do with role={0}'.format(role))

        return move
