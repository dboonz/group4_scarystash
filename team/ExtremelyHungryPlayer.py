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
    def compute_food_score(self, distance_decay=1.5):
        """ Compute: distance to every pill, first step for every pill. 
            Out: dict of step options weighed by distance """
         #initialise a dict of step options: {next_cell: weight_count}

        # loop through the list of available pills
        for p in self.enemy_food:
            # compute the path to the next one
            path_to_pill = self.adjacency.a_star(self.current_pos, p)
            # compute the length for scaling
            weight = np.exp(-len(path_to_pill)/distance_decay)

            # populate the step options dict
            self.step_options[path_to_pill[-1]]+=weight

    

    def compute_optimal_move(self):
        """ Compute the optimal move based on the coordinate with the highest
        score """
        # recommend the step with the highest score
        recommended_coordinate = max(self.step_options, key=self.step_options.get)
        self.move = diff_pos(self.current_pos, recommended_coordinate)
            
    def get_move(self):
        # check, if food is still present
        self.say("Hungry!")
        if (self.next_food is None
                or self.next_food not in self.enemy_food):
            if not self.enemy_food:
                # all food has been eaten? ok. i’ll stop
                return datamodel.stop
        

            self.next_food = self.rnd.choice(self.enemy_food)


        self.step_options = defaultdict(float)
        self.compute_food_score()
        self.compute_optimal_move()

        try:
           return self.move
        except NoPathException:
            print("Help!")
            return datamodel.stop

def factory():
    return SimpleTeam("The Food Eating Players", FoodEatingPlayer(), FoodEatingPlayer())
