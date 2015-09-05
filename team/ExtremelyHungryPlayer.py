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
            first_step = diff_pos(self.current_pos, path_to_pill[-1])
            # compute the length for scaling
            weight = np.exp(-len(path_to_pill)/distance_decay)

            # populate the step options dict
            self.step_options[first_step]+=weight

    def compute_enemy_score(self, enemy_distance_decay=1.5):
        """Update step_options to avoid the enemy. Currently only resets a
        valus of the step_options to -1 if it means taking the shortest path to
        the enemy. 

        It would be better to try for all the new positions what the shortest
        path difference would be. In this case, if there are two paths that
        allow the bot to be eaten they would both be detected.
        
        """
        x,y = self.current_pos 
        l_coor = (x-1,y)
        r_coor = (x+1,y)
        u_coor = (x,y+1)
        d_coor = (x,y-1)

        possible_positions = [u_coor, l_coor, r_coor, d_coor]

        for e in self.enemy_bots:
            # compute the path to the next move
            if e.noisy:
                continue
                        # check if it is within two steps away
            try:
                path_to_bot = self.adjacency.a_star(self.current_pos, e.current_pos)
            except pelita.graph.NoPathException:
                path_to_bot = []
            if len(path_to_bot) < 3:
                first_step = diff_pos(self.current_pos, path_to_bot[-1])
                self.step_options[first_step] = -1
        #if self.me.index == 1:
        #    import pdb; pdb.set_trace()





#            for p1 in possible_positions:
##                import pdb; pdb.set_trace()
#                try:
#                    path_to_bot = self.adjacency.a_star(p1, e.current_pos)
#                except NoPathException:
#                    path_to_bot = []
#
#
#                weight = -2*np.exp(-len(path_to_bot)**2/
#                        enemy_distance_decay**2)
#                self.step_options[p1] += weight
#
    def compute_optimal_move(self):
        """ Compute the optimal move based on the coordinate with the highest
        score """
        # recommend the step with the highest score
        recommended_step = max(self.step_options, key=self.step_options.get)
        self.move = recommended_step
        #self.move = diff_pos(self.current_pos, recommended_coordinate)
            
    def get_move(self):
        # check, if food is still present
        self.say("ID %d" % self.me.index)
        if (self.next_food is None
                or self.next_food not in self.enemy_food):
            if not self.enemy_food:
                # all food has been eaten? ok. i’ll stop
                return datamodel.stop

        

            self.next_food = self.rnd.choice(self.enemy_food)


        self.step_options = defaultdict(float)
        # initialize the step options to zero for all valid moves.
        # This is important, otherwise the bot will not consider all options
        for lm in self.legal_moves:
            self.step_options[lm] = 0

        self.compute_food_score()
        self.compute_enemy_score()
        self.compute_optimal_move()
        self.print_scores()

        
        try:
           return self.move
        except NoPathException:
            print("Help!")
            return datamodel.stop
    
    def print_scores(self):
        """ Print the energy landscape for the next part """
        # compute the indices
        x,y = self.current_pos 

        l_coor = self.step_options[(-1,0)]
        r_coor = self.step_options[(1,0)]
        u_coor = self.step_options[(0,1)]
        d_coor = self.step_options[(0,-1)]
#        scores = map(self.step_options.get, (u_idx, l_idx, r_idx, d_idx))

        print_str = """
              %3.2f   
        %3.2f       %3.2f
              %3.2f""" % (u_coor, l_coor, r_coor, d_coor)

        print(print_str)
        print("Direction: ", self.move)

def factory():
    return SimpleTeam("The Food Eating Players", FoodEatingPlayer(), FoodEatingPlayer())
