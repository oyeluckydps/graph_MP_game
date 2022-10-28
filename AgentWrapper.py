
class AgentWrapper:
    '''
    This class provides the outer blueprint for the Agents. It consists of some common information available to all
    agents.
    You must inherit your implementation of Agent from this class.
    '''
    def __init__(self, io_description, training_rounds, evaluation_rounds):
        '''
        :param io_description: Input/Ouptut for agents descriptor.
        :param training_rounds: Number of training rounds.
        :param evaluation_rounds: Number of evaluation rounds.
        '''
        self.__sim_no = 0
        self.io_desc = io_description
        self.training_rounds = training_rounds
        self.evaluation_rounds = evaluation_rounds
        self.sim_step_no = 0
