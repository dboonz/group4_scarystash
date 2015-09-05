# -*- coding: utf-8 -*-

from pelita import datamodel
import pelita
from pelita.graph import AdjacencyList, NoPathException, diff_pos
from pelita.player import AbstractPlayer, SimpleTeam
import numpy as np
from collections import defaultdict
from .utils.helper import add_pos



class ExtremelyHungryPlayer(AbstractPlayer):
    def set_initial(self):
        self.adjacency = AdjacencyList(self.current_uni.reachable([self.initial_pos]))
        self.next_food = None

    def goto_pos(self, pos):
        return self.adjacency.a_star(self.current_pos, pos)[-1]

    def compute_food_score(self, distance_decay=2.5):
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
        
        """
        decay_per_distance = lambda d: \
                        -2*np.exp(-d**2/enemy_distance_decay**2)
        self.repulse_bot(self.enemy_bots, decay_per_distance) 


    def repulse_bot(self, bot_list, function):
        '''In: list of bots to repulse, repulsion function 
        '''
        # get the possible positions
        for lm in self.legal_moves:
            # The position we would be in in this case "possible_position"
            p_pos = add_pos(self.current_pos, lm)
            for e in bot_list:
                # compute the path to the next move
                try:
                    if e.noisy:
                        continue
                except AttributeError:
                    pass
                try:
                    path_to_bot = self.adjacency.a_star(p_pos, e.current_pos)
                except pelita.graph.NoPathException:
                    path_to_bot = []
                distance = len(path_to_bot)
                self.step_options[lm] += function(distance)


    def compute_friend_score(self):
        '''Based on the friend_bot, decay function '''
        d_decay = 5
        max_repulsion = 1.1*self.step_options[max(self.step_options)]
        decay_function= lambda d: -max_repulsion*np.exp(-d**2 / d_decay**2)
        self.repulse_bot(self.other_team_bots, decay_function)
        


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
        self.compute_friend_score()
        self.compute_optimal_move()
        if self.me.index == 0:
            self.print_scores()
       #import pdb; pdb.set_trace()
        
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
        u_coor = self.step_options[(0,-1)]
        d_coor = self.step_options[(0,1)]
        c_coor = self.step_options[(0,0)]
#        scores = map(self.step_options.get, (u_idx, l_idx, r_idx, d_idx))

        print_str = """
                %3.2f   
        %3.2f   %3.2f    %3.2f
                %3.2f""" % (u_coor, l_coor, c_coor, r_coor, d_coor)

        print(print_str)
        print("Direction: ", self.move)

def factory():
    return SimpleTeam("The Food Eating Players", FoodEatingPlayer(), FoodEatingPlayer())
