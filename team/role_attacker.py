# -*- coding: utf-8 -*-

import numpy as np
import pelita
from pelita import datamodel
from pelita.graph import AdjacencyList, NoPathException, diff_pos
from collections import defaultdict
from .utils.helper import add_pos


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
        self.past_moves = []
        self.loop_counter = 0

    def goto_pos(self, pos):
        return self.player.adjacency.a_star(self.current_pos, pos)[-1]


    def detect_loop(self):
        """ Detects if we have a loop, and writes out that we're in a loop """
        if len(set(self.past_moves[-20:-1])) < 10:
            if len(self.past_moves) > 18:
                self.loop_counter += 1
        else:
            self.loop_counter = 0

#        if self.player.me.index == 1:
#            import pdb; pdb.set_trace()
        return True

    def compute_food_score(self, distance_decay=2.5):
        """ Compute: distance to every pill, first step for every pill. 
            Out: dict of step options weighed by distance """
         #initialise a dict of step options: {next_cell: weight_count}

        # loop through the list of available pills
        distances = np.zeros(len(self.player.enemy_food))
        i = 0
        for p in self.player.enemy_food:
            # compute the path to the next one
            path_to_pill = self.player.adjacency.a_star(self.player.current_pos, p)
            first_step = diff_pos(self.player.current_pos, path_to_pill[-1])
            # compute the length for scaling
            distance = len(path_to_pill)
            distances[i] = distance
            weight = np.exp(-distance/distance_decay)

            # populate the step options dict
            self.step_options[first_step]+=weight

            i += 1
        if self.loop_counter > 3:
            #print("Stuck in a loop for %d steps" % self.loop_counter)
            distances_idx = np.argsort(distances)
            for i in range(min(int((self.loop_counter - 10)/3), len(distances_idx))):
                path_to_pill = \
                    self.player.adjacency.a_star(self.player.current_pos,
                    self.player.enemy_food[distances_idx[i]])
                first_step = diff_pos(self.player.current_pos, path_to_pill[-1])
                # compute the length for scaling
                distance = len(path_to_pill)
                weight = np.exp(-distance/distance_decay)

                # populate the step options dict
                self.step_options[first_step]-=weight
            
#        if self.loop_counter > 20 and self.player.me.index == 0:
#            import pdb; pdb.set_trace()



    def compute_enemy_score(self, enemy_distance_decay=2.3):
        """Update step_options to avoid the enemy. Currently only resets a
        values of the step_options to -1 if it means taking the shortest path to
        the enemy. 
        
        """
        decay_per_distance = lambda d: \
                    -3*np.exp(-d**2/enemy_distance_decay**2)

        self.repulse_bot(self.player.enemy_bots, decay_per_distance) 

    def repulse_bot(self, bot_list, function):
        '''In: list of bots to repulse, repulsion function 
        '''
        # get the possible positions
        for lm in self.player.legal_moves:
            # The position we would be in in this case "possible_position"
            p_pos = add_pos(self.player.current_pos, lm)
            for e in bot_list:
                # compute the path to the next move
                try:
                    if e.noisy:
                        continue
                except AttributeError:
                    pass
                try:
                    path_to_bot = self.player.adjacency.a_star(p_pos, e.current_pos)
                except pelita.graph.NoPathException:
                    path_to_bot = []
                distance = len(path_to_bot)
                self.step_options[lm] += function(distance)

    def compute_friend_score(self):
        '''Based on the friend_bot, decay function '''
        d_decay = 5
        max_repulsion = 0.01*self.step_options[max(self.step_options)]
        decay_function= lambda d: -max_repulsion*np.exp(-d**2 / d_decay**2)
        self.repulse_bot(self.player.other_team_bots, decay_function)
        

    def compute_optimal_move(self):
        """ Compute the optimal move based on the coordinate with the highest
        score """
        # recommend the step with the highest score
        recommended_step = max(self.step_options, key=self.step_options.get)

        # if we're in a loop: go to the second best move
#        if self.loop_counter > 3:
#            recommended_step = sorted(self.step_options,
#                    key=self.step_options.get,
#                    reverse=True)[1]

        self.move = recommended_step
        #self.move = diff_pos(self.current_pos, recommended_coordinate)
 
    def get_move(self, player):
        self.player = player
        # check, if food is still present
        self.player.say("ID %d" % self.player.me.index)
        if (self.next_food is None
                or self.next_food not in self.player.enemy_food):
            if not self.player.enemy_food:
                # all food has been eaten? ok. i’ll stop
                return datamodel.stop

            self.next_food = self.player.rnd.choice(self.player.enemy_food)


        self.step_options = defaultdict(float)
        # initialize the step options to zero for all valid moves.
        # This is important, otherwise the bot will not consider all options
        for lm in self.player.legal_moves:
            self.step_options[lm] = 0
        
        self.detect_loop()
        self.compute_food_score()
        self.compute_enemy_score()
        self.compute_friend_score()
        self.compute_optimal_move()

        self.past_moves.append(self.player.current_pos)
        #if self.player.me.index == 0:
        #    self.print_scores()
#        import pdb; pdb.set_trace()
        
        try:
           return self.move
        except NoPathException:
            #print("Help!")
            return datamodel.stop
 

    def print_scores(self):
        """ Print the energy landscape for the next part """
        # compute the indices
        x,y = self.player.current_pos 

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

        #print(print_str)
        #print("Direction: ", self.move)

