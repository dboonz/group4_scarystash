# -*- coding: utf-8 -*-

from pelita import datamodel
import pelita
from pelita.graph import AdjacencyList, NoPathException, diff_pos
from pelita.player import AbstractPlayer, SimpleTeam
import numpy as np


class ExtremelyHungryPlayer(AbstractPlayer):
    def set_initial(self):
        self.adjacency = AdjacencyList(self.current_uni.reachable([self.initial_pos]))
        self.next_food = None

    def goto_pos(self, pos):
        return self.adjacency.a_star(self.current_pos, pos)[-1]
#
#    def compute_distance_to_list(_list):
#        a = []
#        for item in _list:
#            a.append(self.adjacency.a_star(
#            
#

    def get_move(self):
        # check, if food is still present
        self.say("Hungry!")
        if (self.next_food is None
                or self.next_food not in self.enemy_food):
            if not self.enemy_food:
                # all food has been eaten? ok. i’ll stop
                return datamodel.stop


            self.next_food = self.rnd.choice(self.enemy_food)
        # make a list of the distances to delicious pills

        self.next_food_distance_list = np.array(list(map(
                lambda x: len(self.adjacency.a_star(self.current_pos, x)),
                 self.enemy_food)))

        minimum_index = np.argmin(self.next_food_distance_list)
        # get the path to the next part of liqorice
        # steps = self.adjacency.a_star(self.current_pos, self.enemy_food[minimum_index])
        # print("Distance to first pill:",  self.next_food_distance_list)
        self.next_food = self.enemy_food[minimum_index]
        try:
            next_pos = self.goto_pos(self.next_food)
            move = diff_pos(self.current_pos, next_pos)
            return move
        except NoPathException:
            print("Help!")
            return datamodel.stop

def factory():
    return SimpleTeam("The Food Eating Players", FoodEatingPlayer(), FoodEatingPlayer())
