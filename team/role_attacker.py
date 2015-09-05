# -*- coding: utf-8 -*-

import numpy as np
from pelita import datamodel
from pelita.graph import AdjacencyList, NoPathException, diff_pos
from collections import defaultdict


class ExtremelyHungryRole():
    '''
    Role of Extremely Hungry.
    '''
    def __init__(self):
        '''
        '''
        self.role_name = 'extremely_hungry'
        self.talk = 'Hungry!'
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

        self.next_food = self.player.rnd.choice(self.player.enemy_food)
        self.step_options = defaultdict(float)
        self.compute_food_score()
        self.compute_optimal_move()
        try:
           return self.move
        except NoPathException:
            print("Help!")
            return datamodel.stop


    def compute_food_score(self, distance_decay=1.5):
        """ Compute: distance to every pill, first step for every pill.
            Out: dict of step options weighed by distance """
         #initialise a dict of step options: {next_cell: weight_count}

        # loop through the list of available pills
        for p in self.player.enemy_food:
            # compute the path to the next one
            path_to_pill = self.player.adjacency.a_star(self.player.current_pos, p)
            # compute the length for scaling
            weight = np.exp(-len(path_to_pill)/distance_decay)
            # populate the step options dict
            self.step_options[path_to_pill[-1]]+=weight


    def compute_optimal_move(self):
        """ Compute the optimal move based on the coordinate with the highest
        score """
        # recommend the step with the highest score
        recommended_coordinate = max(self.step_options, key=self.step_options.get)
        self.move = diff_pos(self.player.current_pos, recommended_coordinate)
