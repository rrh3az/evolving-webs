from copy import copy
from attr import attr, attrib
import networkx as nx
# import model
import random
import copy

class Species:
    def __init__(self, name, index, current_pop, prev_pop, resources, death_rate, is_extinct=False):
        self._name = name
        self._index = index # node idex in digraph
        self._current_pop = current_pop # population at current time t
        self._prev_pop = prev_pop # previous population at time t-1
        self._resources = resources # current resource count
        self._death_rate = death_rate # species death rate
        self._attributes = random.sample(range(0, 500), 10) # random selection of 10 attributes
        self._is_extinct = is_extinct 

    # getter methods
    def get_name(self):
        return self._name

    def get_index(self):
        return self._index
    
    def get_current_pop(self):
        return self._current_pop

    def get_prev_pop(self):
        return self._prev_pop

    def get_resources(self):
        return self._resources

    def get_death_rate(self):
        return self._death_rate

    def get_attributes(self):
        return self._attributes


    # setter methods
    def set_name(self, name):
        self._name = name

    def set_index(self, index):
        self._index = index

    def set_current_pop(self, current_pop):
        self._current_pop = current_pop

    def set_prev_pop(self, prev_pop):
        self._prev_pop = prev_pop

    def set_resources(self, resources):
        self._resources = resources

    def set_death_rate(self, death_rate):
        self._death_rate = death_rate

    def set_attributes(self, attributes):
        self._attributes = attributes

    # Misc. methods
    def make_extinct(self):
        self._is_extinct = True

    # makes child species from current species
    def gen_child_species(self):
        child = copy.copy(self) # copying original node
        new_attribs = self.get_attributes() # editing attributes
        new_attribs[random.randrange(1, 10)] = random.randrange(500) # one random attribute set to new random attribute
        child.set_attributes(new_attribs)
        return child