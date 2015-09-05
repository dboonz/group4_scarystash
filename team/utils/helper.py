# -*- coding: utf-8 -*-

# This would be a good place for utility functions.
class CollectiveMemory():
    """Implement a collective memroy of the two players.

    A collective memory that the two players share, Can also be used as a hack to access player1 with player2
    and vice versa. (Bot1.memory.bot2 will return Bot2)
    """
    def __init__(self,bot1=None, bot2=None):
        self._bot1 = bot1
        self._bot2 = bot2
        self.brain = {}
        if bot1 is not None:
            bot1.set_memory(self)
        if bot2 is not None:
            bot2.set_memory(self)

    @property
    def bot1(self):
        return self._bot1

    @bot1.setter
    def bot1(self, value):
        self._bot1 = value
        
    @property
    def bot2(self):
        return self._bot2

    @bot2.setter
    def bot2(self, value):
        self._bot2 = value

    def store(self, key, value):
        """Store something in the collective memory

        :param key: key of the memory to be stored
        :param value: memory to be stored
        :return:True if storage was successful, False otherwise
        """
        try:
            self.brain[key] = value
            return True
        except:
            return False

    def retrieve(self, key):
        """ Retrieve a memory
        :param key: key of memory to be retrieved
        :return: stored memory, None if memory does not exist
        """
        if not key in self.brain:
            return None
        else:
            return self.brain[key]


def add_pos(p1, p2):
    """ Add two positions. Each position is defined as a tuple of (int, int)"""
    return p1[0]+p2[0], p1[1]+p2[1]

def utility_function():
    pass
