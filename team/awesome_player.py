# -*- coding: utf-8 -*-

# (Specifying utf-8 is always a good idea in Python 2.)


from pelita.player import AbstractPlayer


class AwesomePlayer(AbstractPlayer):
    '''
    Player which makes awesome move decisions.
    '''
    def __init__(self, walkie_talkie=None):
        '''
        '''
        self.memory = walkie_talkie
        self.attacker = Attacker()
        self.defender = Defender()


    def get_role(self):
        '''Returns the role of the player.
        '''
        if self.memory is None:
            pass
        else:
            pass


    def get_move(self):
        '''Returns the next move to be made by the player.
        '''
        role = self.get_role()

        if role is 'attack':
            self.attacker.get_move()

        elif role is 'defend':
            self.defender.get_move()

        else:
            raise ValueError('Donnot know what to do with role={0}'.format(role))
