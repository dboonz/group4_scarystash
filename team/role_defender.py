# -*- coding: utf-8 -*-

import numpy as np
from pelita import datamodel
from pelita.graph import AdjacencyList, NoPathException, diff_pos
from collections import defaultdict


class PossessiveItalianRole():
    '''
    '''
    def __init__(self):
        '''
        '''
        self.role_name = 'possessive_italian'
        self.talk = 'Go Away!'
        self.next_food = None
        self.player = None

    def get_move(self, player):
        '''
        '''
        self.player = player

        if (self.next_food is None) or (self.next_food not in self.player.enemy_food):
            if not self.player.enemy_food:
                # all food has been eaten? ok. i’ll stop
                return datamodel.stop

        index_enemy_to_block = self.get_enemy_to_block()
        path_en_to_all_food = self.get_closest_food_to_enemy(index_enemy_to_block)
        intercept = self.get_point_to_intercept(path_en_to_all_food)

        try:
            next_pos = self.goto_pos(intercept)
            move = diff_pos(self.player.current_pos, next_pos)
            return move
        except NoPathException:
            print("Help!")
            return datamodel.stop


    def get_enemy_to_block(self):
        '''Returns the index of the closest enemy.
        '''
        my_pos = self.player.current_pos
        en_bots = self.player.enemy_bots
        dist_en0 = len(self.player.adjacency.a_star(my_pos, en_bots[0].current_pos))
        dist_en1 = len(self.player.adjacency.a_star(my_pos, en_bots[1].current_pos))
        return np.argmin([dist_en0, dist_en1])

    def get_closest_food_to_enemy(self, en_index):
        '''Return the closest food to the enemy.
        '''
        # enemy position
        en_pos = self.player.enemy_bots[en_index].current_pos
        # distance of enemy to all food
        distance = lambda x: self.player.adjacency.a_star(en_pos, x)
        path_en_to_food = list(map(distance, self.player.team_food))
        path_en_to_all_food = np.sort(path_en_to_food)
        return path_en_to_all_food

    def get_point_to_intercept(self, path_en_to_all_food):
        '''Point to intercept
        '''
        path = path_en_to_all_food[0]
        if len(path) == 0:
            path = path_en_to_all_food[1]
        # calculate the intercept of path
        index = np.round(len(path) / 2).astype(int)
        intercept = path[index]
        return intercept

    def goto_pos(self, pos):
        '''Return the maze coordinate of the 1st step toward pos'''
        distances = self.player.adjacency.a_star(self.player.current_pos, pos)
        if len(distances) > 0:
            return distances[-1]
        else:
            return self.player.current_pos
