import pandas as pd
from random import randint as randi
import random

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
