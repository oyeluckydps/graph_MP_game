
class PGnode:
    '''
    Class to hold the node and associated agent for the game.
    '''
    def __init__(self, name, Agent=None):
        self.name = name
        if Agent is not None:
            self._Agent = Agent()
        else:
            self._Agent = None
        self._output_this_round = None
        self.output = None
        self.incoming_nodes = []
        self.outgoing_nodes = []
        self.incoming_log = []
        self.outgoing_log = []

    def add_incoming_nodes(self, nodes_list):
        '''
        :param nodes_list: A list or single node element that has to be added to the incoming list.
        :return: self
        '''
        if type(nodes_list) == list:
            self.incoming_nodes += nodes_list
        else:
            self.incoming_nodes.append(nodes_list)

    def remove_incoming_node(self, node):
        self.incoming_nodes.remove(node)

    def add_outgoing_nodes(self, nodes_list):
        '''
        :param nodes_list: A list or single node element that has to be added to the outgoing list.
        :return: self
        '''
        if type(nodes_list) == list:
            self.outgoing_nodes += nodes_list
        else:
            self.outgoing_nodes.append(nodes_list)

    def remove_outgoing_node(self, node):
        self.outgoing_nodes.remove(node)

    def set_incoming_operator(self, Agent):
        self._Agent = Agent

    def process_node(self, round_no):
        '''
        Take the input from incoming nodes and set the _output_this_round
        :param round_no: Simulation step count.
        :return: self
        '''
        incoming_values = [incoming_edge.output for incoming_edge in self.incoming_nodes]
        self.incoming_log += incoming_values    # Log the incoming values to be used for perfomance evaluation of the agent.
        self._output_this_round = self._Agent.process(incoming_values, round_no)

    def enact_value(self, round_no):
        '''
        The function puts output of this round into the output accessible to other nodes.
        :param round_no: Simulation step count.
        :return:
        '''
        self.output = self._output_this_round
        self.outgoing_log.append(self.output)   #Log the output of agents too.
        self._output_this_round = None

    def __str__(self, prefix = '', indent = '\t'):
        all_members = [a for a in dir(self) if not (a.startswith('__') and a.endswith('__')) and not callable(getattr(self, a))]
        total_indent = prefix + indent
        node_name = prefix + "Node: " + str(self.name) + '\n'
        message = node_name
        for member in all_members:
            message += str(member) + ' = ' + str(self.__getattribute__(member)) + '\n'
        message = message[:-1]
        message = message.replace('\n', '\n'+total_indent)
        return message

    def __repr__(self):
        return '<'+str(self.name)+'>'