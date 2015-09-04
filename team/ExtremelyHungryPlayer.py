# -*- coding: utf-8 -*-

from pelita import datamodel
import pelita
from pelita.graph import AdjacencyList, NoPathException, diff_pos
from pelita.player import AbstractPlayer, SimpleTeam
import numpy as np
from collections import defaultdict



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
    def compute_adjacency_list(self):
        """ Compute: distance to every pill, first step for every pill. 
            Out: dict of step options weighed by distance """
         #initialise a dict of step options: {next_cell: weight_count}
        self.step_options = defaultdict(float)

        # loop through the list of available pills
        for p in self.enemy_food:
            # compute the path to the next one
            path_to_pill = self.adjacency.a_star(self.current_pos, p)
            # compute the length for scaling
            #weight = 1./len(path_to_pill)
            #weight = 1./len(path_to_pill)**2
            weight = np.exp(-len(path_to_pill)/1.5)

            # populate the step options dict
            self.step_options[path_to_pill[-1]]+=weight
            #recommend the step with ??A

        
        recommended_coordinate = max(self.step_options, key=self.step_options.get)
        self.move = diff_pos(self.current_pos, recommended_coordinate)
        print(recommended_coordinate)
            

    def get_move(self):
        # check, if food is still present
        self.say("Hungry!")
        if (self.next_food is None
                or self.next_food not in self.enemy_food):
            if not self.enemy_food:
                # all food has been eaten? ok. i’ll stop
                return datamodel.stop


            self.next_food = self.rnd.choice(self.enemy_food)

        self.compute_adjacency_list()#get_adjacency_list()
        # now, scale their importance with the distance
        #self.next_food_importance_list =
        #    np.exp(-next_food_distance_list/self.decay_distance)

        # 

###        minimum_index = np.argmin(self.next_food_distance_list)
###        # get the path to the next part of liqorice
###        # steps = self.adjacency.a_star(self.current_pos, self.enemy_food[minimum_index])
###        # print("Distance to first pill:",  self.next_food_distance_list)
###        self.next_food = self.enemy_food[minimum_index]
        try:
#            next_pos = self.goto_pos(self.next_food)
#            print(next_pos)
#            move = diff_pos(self.current_pos, next_pos)
#            print(move)
            return self.move
        except NoPathException:
            print("Help!")
            return datamodel.stop

def factory():
    return SimpleTeam("The Food Eating Players", FoodEatingPlayer(), FoodEatingPlayer())
