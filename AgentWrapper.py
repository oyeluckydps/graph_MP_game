from abc import ABC, abstractmethod
from IOdatatype import IOdatatype

class AgentCommonInformation:
    '''
    It consists of some common information available to all
    agents.
    '''
    def __init__(self, io_description = IOdatatype(), training_rounds = 16000, evaluation_rounds = 4000):
        '''
        :param io_description: Input/Ouptut for agents descriptor.
        :param training_rounds: Number of training rounds.
        :param evaluation_rounds: Number of evaluation rounds.
        '''
        self.__sim_no = 0
        self.__io_desc = io_description
        self.__training_rounds = training_rounds
        self.__evaluation_rounds = evaluation_rounds
        self.__sim_step_no = 0

    @property
    def io_type(self):
        return self.__io_desc.io_type

    @property
    def io_topo(self):
        return self.__io_desc.topo

    @property
    def io_min(self):
        return self.__io_desc.min

    @property
    def io_max(self):
        return self.__io_desc.max

    @property
    def all_elems(self):
        return self.__io_desc.all_elems

    @property
    def io_norm(self):
        return self.__io_desc.norm

    @property
    def training_rounds_count(self):
        return self.__training_rounds

    @property
    def evaluation_rounds_count(self):
        return  self.__evaluation_rounds

    @property
    def sim_step_no(self):
        return self.__sim_step_no

    @property
    def round_type(self):
        if self.sim_step_no < self.__training_rounds:
            return 'training'
        else:
            return 'evaluation'

    @property
    def is_training(self):
        return self.sim_step_no < self.__training_rounds

    @property
    def is_evaluation(self):
        return not (self.is_training)

    @property
    def total_rounds_count(self):
        return self.training_rounds_count + self.evaluation_rounds_count

    def _reset_playground(self):
        self.__sim_no = 0
        self.__sim_step_no = 0

    def _next_simulation(self):
        self.__sim_no += 1

    def _take_a_sim_step(self):
        if self.sim_step_no == self.total_rounds_count-1:
            self.__sim_step_no = 0
            self._next_simulation()
        else:
            self.__sim_step_no += 1

    def _get_diff(self, target, input):
        """
        :param target: The target value/s against which input diff is to be calculated.
        :param input: The input/achieved value.
        :return: The difference according to IO and nor.
        """
        return self.__io_desc.diff_calc(target, input)

    def _get_norm(self, diff):
        """
        :param diff: The difference vector
        :return: Norm of the diff according to IO metric.
        """
        return self.__io_desc.norm_fn(diff)

    def __str__(self, prefix = '', indent = '\t'):
        all_members = [a for a in dir(self) if not (a.startswith('__') and a.endswith('__')) and not callable(getattr(self, a))]
        total_indent = prefix + indent
        message = "******** AgenetCommonInformation ********"  + '\n'
        for member in all_members:
            message += str(member) + ' = ' + str(self.__getattribute__(member)) + '\n'
        message = message[:-1]
        message = message.replace('\n', '\n'+total_indent)
        return message

    def __repr__(self):
        return self.__str__()


class AgentAbstract(ABC):
    '''
    This class provides the outer blueprint for the Agents. You must inherit your implementation of Agent from this class.
    '''

    '''
    You are expected to fully utilize all the properties of AgentCommonInformation member through Common_Data
    element of this class.
    '''
    Common_Data = AgentCommonInformation()

    @abstractmethod
    def __init__(self, target):
        '''
        :param target: Value of the target for agent.

        The agent will always be initiated with a target value.
        '''
        pass

    @abstractmethod
    def process(self, incoming_values, round_no):
        '''
        :param incoming_values: Values from different incoming nodes.
        :param round_no: current simulation step/round number.
        :return: output value that adheres to IO_desc

        In the 0th round a list of [None]*k will be passed for incoming_values and 0 will be passed for round_no. You are
        expected to get the number of incoming nodes from the length of incoming_values.
        '''
        pass

    @abstractmethod
    def new_target(self, new_target):
        '''
        Put the action to be taken when a new target is assigned. This is expected for a new simulation.
        '''
        pass

    def get_diff(self, target, input):
        """
        :param target: The target value/s against which input diff is to be calculated.
        :param input: The input/achieved value.
        :return: The difference according to IO and nor.
        """
        return self.Common_Data._get_diff(target, input)

    def get_norm(self, diff):
        """
        :param diff: The difference vector
        :return: Norm of the diff according to IO metric.
        """
        return self.Common_Data._get_norm(diff)


if __name__ == '__main__':
    distinct_io = IOdatatype(io_type = 'Z', io_topograph = 'distinct', io_range_min = 1, io_range_max = 10, evaluation_norm = 0)
    distinct_setup = AgentCommonInformation(io_description = distinct_io, training_rounds = 15, evaluation_rounds = 10)
    AgentAbstract.Common_Data = distinct_setup
    Agent_007 = sample_Agent(7)
    Agent_007.process([None, None, None], 0)
    Agent_007.process([1, 3, 0], 1)
    print(distinct_io)
    print(distinct_setup)
    pass