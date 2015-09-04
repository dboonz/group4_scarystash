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
        print('Starting memory with {b1} and {b2}'.format(b1 = bot1.__repr__, b2 = bot2.__repr__))
        self.brain = {'step': 1}
        bot1.set_memory(self)
        bot2.set_memory(self)

    def get_bot1(self):
        return self._bot1

    def set_bot1(self, value):
        self._bot1 = value

    def get_bot2(self):
        return self._bot2


    def set_bot2(self, value):
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


def utility_function():
    pass
    # print "Doing some hard work in this function."


