# -*- coding: utf-8 -*-

# (Specifying utf-8 is always a good idea in Python 2.)

import numpy as np
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
        self.round = 0
        self.was_home = True
        self.roles = []
        # True, if any of the enemy bits are harvesters in this round
        self.enemies_attacking = []
        self.sit = False

    def set_initial(self):
        '''Sets the initial values.
        '''
        self.adjacency = AdjacencyList(self.current_uni.reachable([self.initial_pos]))
        self.memory.store((self._index, 'roles'), self.roles)
        self.memory.store((self._index, 'sit'), self.sit)

    def get_role(self):
        '''Returns the role of the player.
        '''
        other_player = self.other_team_bots[0].index
        diff_score = self.team.score - self.enemy_team.score

        if self.round == 0:
            return 'attack'

        elif (not self.was_home) and (self.initial_pos == self.current_pos):
            # You are born at home again
            enemy_pos = np.array([bot.current_pos[1] for bot in self.enemy_bots])
            # If there is any enemy in your field
            if any([bot.is_harvester for bot in self.enemy_bots]):
                other_player = self.other_team_bots[0].index
                # check whether the teammate is defending or attacking
                if self.memory.retrieve((other_player, 'roles'))[-1] == 'defend':
                    return 'attack'
                else:
                    diff_score = self.team.score - self.enemy_team.score
                    if diff_score > len(self.team_food) - 7:
                        return 'defend'
                    else:
                        return 'attack'
            else:
                return 'attack'

        # if a bot was defender for 5 rounds and there was no harvester bot during that time, attack again
        # if self.round > 0 and self.roles[-6:-1] == 'defend' and not np.any(self.enemies_attacking[-6:-1]):
        #     return 'attack'


        if self.memory.retrieve((other_player, 'sit')) == True:
            return 'defend'

        # diff_score = self.team.score - self.enemy_team.score
        # if diff_score > len(self.team_food) - 7:
        #     return 'defend'

        # elif self.roles[-1] == 'attack':
        #     diff_score = self.team.score - self.enemy_team.score
        #     if diff_score > 0:
        #         return 'attack'
        #     else:
        #         self.team_food
        # elif self.roles[-1] == 'defend':
        #     if self.team.score > self.enemy.score:
        #         return 'defend'
        #     else:

        return 'attack'


    def get_move(self):
        '''Returns the next move to be made by the player.
        '''
        # specify the role
        role = self.get_role()
        self.roles.append(role)
        self.enemies_attacking.append(any([bot.is_harvester for bot in self.enemy_bots]))

        if role is 'attack':
            self.say(self.attacker.talk)
            move = self.attacker.get_move(player=self)

        elif role is 'defend':
            self.say(self.defender.talk)
            move = self.defender.get_move(player=self)

        else:
            raise ValueError('Donnot know what to do with role={0}'.format(role))

        self.round += 1
        # Are you in home or field?
        self.was_home = self.me.is_destroyer
        return move
