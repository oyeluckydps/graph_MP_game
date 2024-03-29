import pandas as pd
from random import randint as randi
import random
from itertools import product
from pathlib import Path

from AgentWrapper import AgentAbstract
import memory_map as mm

class target_returning_Agent(AgentAbstract):
    '''
    A dumb sample agent that always outputs a single value that is the maximum permissible value.
    '''
    def __init__(self, target):
        Common_Data = AgentAbstract.Common_Data
        self.target = target
        if Common_Data.io_type == 'B':
            self.always_output = 2**Common_Data.io_max - 1
        else:
            self.always_output = Common_Data.io_max

    def process(self, incoming_values, round_no):
        if round_no == 0:
            self.num_incoming_nodes = len(incoming_values)
        if round_no:
            last_diff = AgentAbstract.get_diff(AgentAbstract, self.target, incoming_values)
            last_score = AgentAbstract.get_norm(AgentAbstract, last_diff)
        return self.always_output

    def new_target(self, new_target):
        self.target = new_target


class random_Agent(AgentAbstract):
    '''
    A dumb sample agent that always outputs a single value that is the maximum permissible value.
    '''
    def __init__(self, target):
        Common_Data = AgentAbstract.Common_Data
        self.target = target
        if Common_Data.io_type == 'B':
            self.type, self.min, self.max = 'Z', 0, 2**Common_Data.io_max - 1
        elif Common_Data.io_type == 'Z':
            self.type, self.min, self.max = 'Z', Common_Data.io_min, Common_Data.io_max
        else:
            self.type, self.min, self.max = 'R', Common_Data.io_min, Common_Data.io_max

    def process(self, incoming_values, round_no):
        if self.type == 'Z':
            return randi(self.min, self.max)
        else:
            return random.uniform(self.min, self.max)

    def new_target(self, new_target):
        self.target = new_target


class fixed_map_Agent(AgentAbstract):
    '''
    A dumb sample agent that always outputs value based on a fixed, non-evolving map from input to output.
    The map is independent of target.
    '''
    def __init__(self, target, MM_format):
        Common_Data = AgentAbstract.Common_Data
        self.target = target

        if Common_Data.io_type == 'B':
            self.type, self.min, self.max = 'Z', 0, 2**Common_Data.io_max - 1
        elif Common_Data.io_type == 'Z':
            self.type, self.min, self.max = 'Z', Common_Data.io_min, Common_Data.io_max
        else:
            raise TypeError("Real type is not supported with fixed_map_Agent!")

        self._incoming_edges_count = None
        self._path_prefix = Path('')
        self._my_name = None

        self._memory_map = mm.memoryMap(MM_format, Common_Data)

    @property
    def my_name(self):
        return self._my_name

    @my_name.setter
    def my_name(self, name):
        self._my_name = str(name)

    @property
    def path_prefix(self):
        return self._path_prefix

    @path_prefix.setter
    def path_prefix(self, path_prefix):
        self._path_prefix = Path(path_prefix)

    @property
    def incoming_edges_count(self):
        return self._incoming_edges_count

    @incoming_edges_count.setter
    def incoming_edges_count(self, num_edges):
        self._incoming_edges_count = num_edges

    def save_curr_map(self):
        # Save Map
        folder_add = self._path_prefix
        folder_add.mkdir(parents=True, exist_ok=True)
        with open(folder_add / Path('map_of_' + str(self._my_name) + '.txt'), 'w') as f:
            f.write('I am ' + str(self._my_name) + '.\n')
            for ic, ou in self._memory_map.MM.items():
                f.write(f"{ic}: {ou}\n")

    def set_fix_map(self, MM, save_map = False):
        self._memory_map.set_memory_map(MM=MM)
        if save_map:
            self.save_curr_map()

    def reset_fix_map(self, save_map = False):
        self._memory_map.reset_memory_map()
        if save_map:
            self.save_curr_map()

    def process(self, incoming_values, round_no):
        if not round_no:        # Round 0
            return randi(self.min, self.max)
        return self._memory_map.MM[tuple(incoming_values)]

    def new_target(self, new_target):
        self.target = new_target