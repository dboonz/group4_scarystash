# -*- coding: utf-8 -*-

# (Specifying utf-8 is always a good idea in Python 2.)


from pelita.player import AbstractPlayer


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
        '''
        '''
        if self.attacker is not None:
            self.attacker._set_index(self._index)
            self.attacker._set_initial(self.universe_states[-1], self._current_state)

         # if self.defender is not None:
         #    self.defender.set_initial(self.current_uni)

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
        print('GETTING MOVE', self._index)
        role = self.get_role()

        if role is 'attack':
            move = self.attacker.get_move()
            return move

        elif role is 'defend':
            return self.defender.get_move()

        else:
            raise ValueError('Donnot know what to do with role={0}'.format(role))
