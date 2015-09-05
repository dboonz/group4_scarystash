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


        #self.get_enemy_to_block()
        index_enemy_to_block = self.get_enemy_to_block()
        food, path = self.get_closest_food_to_enemy(index_enemy_to_block)
        #self.get_closest_food()
        #self.get_food_to_protect()
        #self.get_enemy_path()
        #self.get_point_to_intercept()
        intercept = self.get_point_to_intercept(path)

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
        #self.enemy_to_block = np.argmin([dist_enemy0, dist_enemy1])

    def get_closest_food_to_enemy(self, en_index):
        '''Return the closest food to the enemy.
        '''
        # enemy position
        en_pos = self.player.enemy_bots[en_index].current_pos
        # distance of enemy to all food
        distance = lambda x: self.player.adjacency.a_star(en_pos, x)
        path_en_to_food = list(map(distance, self.player.team_food))
        dist_en_to_food = [len(path) for path in path_en_to_food]
        # food to protect
        index = np.argmin(dist_en_to_food)  #
        food = self.player.team_food[index] #position of food in tuple
        path = path_en_to_food[index]       #path from enemy to food in list of tuples
        return food, path

    def get_point_to_intercept(self, path):
        '''Point to intercept
        '''
        if len(path) > 0:
            index = np.round(len(path) / 2).astype(int)
            intercept = path[index]
        else:
            print("I AM HERE!!!!")
            intercept = self.player.current_pos
        return intercept

        # if len(self.enemy_path) > 0:
        #     index = np.round(len(self.enemy_path)/2)
        #     self.p_intercept = self.enemy_path[index.astype(int)]
        # else:
        #     while len(self.enemy_path) == 0:
        #         self.enemy_next_food_distance_list = np.delete(self.enemy_next_food_distance_list, self.minimum_index)
        #         self.get_food_to_protect()
        #         self.get_enemy_path()
        #         index = np.round(len(self.enemy_path)/2)
        #         self.p_intercept = self.enemy_path[index.astype(int)]


    def goto_pos(self, pos):
        '''Return the maze coordinate of the 1st step toward pos'''
        distances = self.player.adjacency.a_star(self.player.current_pos, pos)
        if len(distances) > 0:
            return distances[-1]
        else:
            return self.player.current_pos
