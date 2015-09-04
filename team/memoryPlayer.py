# -*- coding: utf-8 -*-

# (Specifying utf-8 is always a good idea in Python 2.)
from os import wait

from pelita.player import AbstractPlayer
from pelita.datamodel import stop
from pelita.datamodel import Bot
import time

# use relative imports for things inside your module
import numpy.random
from .utils import utility_function
from .utils.helper import CollectiveMemory

class MemoryPlayer(AbstractPlayer):
    """ Basically a clone of the RandomPlayer. """

    def __init__(self, is_sender=False, memory=None):
        # Do some basic initialisation here. You may also accept additional
        # parameters which you can specify in your factory.
        # Note that any other game variables have not been set yet. So there is
        # no ``self.current_uni`` or ``self.current_state``
        self.sleep_rounds = 0
        self.memory = memory
        self.is_sender = is_sender


    def set_initial(self):
        # Now ``self.current_uni`` and ``self.current_state`` are known.
        # ``set_initial`` is always called before ``get_move``, so we can do some
        # additional initialisation here

        # Just printing the universe to give you an idea, please remove all
        # print statements in the final player.
        print(self.current_uni.pretty)

    def set_memory(self, memory):
        self.memory = memory
        print(str(self.__repr__) + 'setting memory to'+ str(self.memory.__repr__))

    def check_pause(self):
        # make a pause every fourth step because whatever :)
        if self.sleep_rounds <= 0:
            if self.rnd.random() > 0.75:
                self.sleep_rounds = 3

        if self.sleep_rounds > 0:
            self.sleep_rounds -= 1
            texts_def = ["Don't come near!", "This is Sparta!!", "BooooOOoo"]
            texts_eat = ["Om nom nom", "BANANA!!"]

            if self.me.is_destroyer:
                self.say(self.rnd.choice(texts_def))
            else:
                self.say(self.rnd.choice(texts_eat))
            return stop


    def get_move(self):

        if self.memory is not None:
            step = None
            # the sender always increases the step count
            step = self.memory.retrieve('step')
            #print(step)
            if self.is_sender:
                if step is not None:
                    self.memory.store('step', step + 1)
                else:
                    self.memory.store('step', 1)
            # the receiver always reports it
            else:
                if step:
                    print('Step:' + str(step))



        utility_function()

        # legal_moves returns a dict {move: position}
        # we always need to return a move
        possible_moves = list(self.legal_moves.keys())
        # selecting one of the moves
        return self.rnd.choice(possible_moves)

