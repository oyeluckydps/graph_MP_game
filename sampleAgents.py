import pandas as pd
from random import randint as randi
import random
from itertools import product
from pathlib import Path

from AgentWrapper import AgentAbstract

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
    def __init__(self, target):
        Common_Data = AgentAbstract.Common_Data
        self.target = target
        if Common_Data.io_type == 'B':
            self.type, self.min, self.max = 'Z', 0, 2**Common_Data.io_max - 1
        elif Common_Data.io_type == 'Z':
            self.type, self.min, self.max = 'Z', Common_Data.io_min, Common_Data.io_max
        else:
            raise TypeError("Real type is not supported with fixed_map_Agent!")
        self.incoming_edges_count = None
        self.name = None
        self.experiment_number = 0

    def set_name(self, name):
        self.name = str(name)

    def reset_fix_map(self):
        if self.incoming_edges_count is not None:
            all_possible_inputs = list(product(list(range(self.min, self.max+1)), repeat=self.incoming_edges_count))
            self.map = {an_input:randi(self.min, self.max) for an_input in all_possible_inputs}
            # Save Map
            folder_add = Path(str(id(AgentAbstract))+'_'+str(self.experiment_number))
            folder_add.mkdir(parents=True, exist_ok=True)
            with open(folder_add / Path('map_of_' + str(self.name) + '_' + str(id(self)) + '.txt'), 'w') as f:
                f.write('I am '+str(self.name)+'.\n')
                for ic, ou in self.map.items():
                    f.write(f"{ic}: {ou}\n")
        else:
            raise('Number of incoming edges is unknown!')
        self.experiment_number += 1

    def process(self, incoming_values, round_no):
        if not round_no:        # Round 0
            self.incoming_edges_count = len(incoming_values)
            self.reset_fix_map()
            return randi(self.min, self.max)
        return self.map.get(tuple(incoming_values))

    def new_target(self, new_target):
        self.target = new_target