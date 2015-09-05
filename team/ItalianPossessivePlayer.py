# -*- coding: utf-8 -*-

from pelita import datamodel
import pelita
from pelita.graph import AdjacencyList, NoPathException, diff_pos
from pelita.player import AbstractPlayer, SimpleTeam
import numpy as np
import time

class ItalianPossessivePlayer(AbstractPlayer):
    def set_initial(self):
        self.adjacency = AdjacencyList(self.current_uni.reachable([self.initial_pos]))
        self.next_food = None

    def goto_pos(self, pos):
        #print(len(self.adjacency.a_star(self.current_pos, pos)))
        if len(self.adjacency.a_star(self.current_pos, pos)) > 0:
            return self.adjacency.a_star(self.current_pos, pos)[-1]
        else:
            return self.current_pos

    # Determine the closest enemy
    def get_enemy_to_block(self):
        dist_enemy0 = len(self.adjacency.a_star(self.current_pos, self.enemy_bots[0].current_pos))
        dist_enemy1 = len(self.adjacency.a_star(self.current_pos, self.enemy_bots[1].current_pos))

        self.enemy_to_block = np.argmin([dist_enemy0, dist_enemy1])
    
    # Determine closest food for that enemy
    def get_closest_food(self):
        self.enemy_next_food_distance_list = np.array(list(map(
                lambda x: len(self.adjacency.a_star(self.enemy_bots[self.enemy_to_block].current_pos, x)),
                 self.team_food)))
    
    # Decide which food to protect
    def get_food_to_protect(self):
        self.minimum_index = np.argmin(self.enemy_next_food_distance_list)
        self.food_to_protect = self.team_food[self.minimum_index]

    # Enemy path
    def get_enemy_path(self):
        self.enemy_path = self.adjacency.a_star(self.enemy_bots[self.enemy_to_block].current_pos, self.food_to_protect)

    # Point to intercept
    def get_point_to_intercept(self):
        if len(self.enemy_path) > 0:
            index = np.round(len(self.enemy_path)/2)
            self.p_intercept = self.enemy_path[index.astype(int)]
        else:
            while len(self.enemy_path) == 0:
                self.enemy_next_food_distance_list = np.delete(self.enemy_next_food_distance_list, self.minimum_index)
                self.get_food_to_protect()
                self.get_enemy_path()
                index = np.round(len(self.enemy_path)/2)
                self.p_intercept = self.enemy_path[index.astype(int)]

    #def sit_on_food(self):
        

    def get_move(self):
        # check, if food is still present
        self.say("Go Away!!")
        if (self.next_food is None
                or self.next_food not in self.enemy_food):
            if not self.enemy_food:
                # all food has been eaten? ok. i’ll stop
                return datamodel.stop

        self.get_enemy_to_block()
        self.get_closest_food()
        self.get_food_to_protect()
        self.get_enemy_path()
        self.get_point_to_intercept()

        try:
            next_pos = self.goto_pos(self.p_intercept)
            move = diff_pos(self.current_pos, next_pos)
            return move
        except NoPathException:
            print("Help!")
            return datamodel.stop

def factory():
    return SimpleTeam("The Italian Players", ItalianPossessivePlayer(), FoodEatingPlayer())
