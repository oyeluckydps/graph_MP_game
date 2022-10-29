
class IOdatatype():
    '''
    A class to handle all datatype for input and output of agents.

    Limitation of the norm implementation: The current norm implementation does not allow for a set of targets to be
    tested against single or set of achieved targets.
    '''
    allowed_io_type = ['Z', 'R', 'B']
    allowed_topo = ['distinct', 'straight', 'ring', 'hypercube']
    allowed_norm_type = ['inf', 0, 'R-0']

    allowed_combination = [
        ('Z', 'distinct', 0),
        ('Z', 'straight', 'inf'),       ('Z', 'straight', 0),       ('Z', 'straight', 'R-0'),
        ('Z', 'ring', 'inf'),           ('Z', 'ring', 0),           ('Z', 'ring', 'R-0'),
        ('R', 'straight', 'inf'),       ('R', 'straight', 0),       ('R', 'straight', 'R-0'),
        ('R', 'ring', 'inf'),           ('R', 'ring', 0),           ('R', 'ring', 'R-0'),
        ('B', 'hypercube', 'inf'),      ('B', 'hypercube', 0),      ('B', 'hypercube', 'R-0')
    ]

    def __init__(self, io_type = 'Z', io_topograph = 'straight', io_range_min = 0, io_range_max = 15, evaluation_norm = 'inf'):
        '''
        :param io_type: Takes input 'Z', 'R', or 'B' to indicate the input and output type. Integral i.e. distinct values are
                        represented by 'Z' while  continuos values for input and output are represented by 'R'. 'B' indicates
                        binary string treatment for IO values.
        :param io_topograph: Takes input as
                            1.) 'distinct' for all elements to be treated as individual elements. This is only supported with
                            'Z' type.
                            2.) 'straight' for all elements to be treated as numbers on number line. Supported with 'Z' and 'R'
                            3.) 'ring' for the elements to be treated as numbers on number line whose ends are joined.
                                Supported with 'Z' and 'R'
                            4.) 'hypercube' for binary string to be treated as nodes of hypercube. Supported with 'B' only.
        :param io_range_min: Included value of Lower bound of range.
        :param io_range_max: Included value of Upper bound of range. In case of 'B' io type it specifies the number of bits in
                                bitstring.
        :param evaluation_norm: Norm for diff calculation. Allowed values are R+ U {'inf'}
        '''

        self.io_type = io_type
        self.topo = io_topograph
        if io_type == 'B':
            self.bits = io_range_max
        else:
            self.min = io_range_min
            self.max = io_range_max

        if type(evaluation_norm) is float or type(evaluation_norm) is int:
            self.norm = evaluation_norm
            if evaluation_norm == 0:
                self.norm_type = 0
            else:
                self.norm_type = 'R-0'
        elif evaluation_norm == 'inf':
            self.norm = float('inf')
            self.norm_type = 'inf'
        else:
            raise ValueError('Invalid value for norm!')

        self.verify_input_params()
        self.set_evaluation_fn()


    def verify_input_params(self):
        if (self.io_type, self.topo, self.norm_type) not in self.allowed_combination:
            raise TypeError("Invalid combination of IO params!")

#------------------------------* Norm Evaluation Related Functions *----------------------------------#
    def set_evaluation_fn(self):
        if self.norm_type == 0:
            self.norm_fn = self.zeroth_norm
        elif self.norm_type == 'inf':
            self.norm_fn = self.inf_norm
        else:
            self.norm_fn = self.default_norm

    def non_list_handling(fn):
        '''
        :return: A wrapper to convert target into list of target with same value for propoer norm evaluation.
        '''

        def handle_list(io_desc, target, achieved):
            if type(target) is not list and type(achieved) is list:
                target = [target] * len(achieved)
                return fn(io_desc, target, achieved)
            elif type(target) is list and type(achieved) is list:
                return fn(io_desc, target, achieved)
        return handle_list

    @non_list_handling
    def diff_calc(io_desc, target, achieved):
        '''
        :return: A wrapper to find the modulo of difference between target and achieved.
        '''

        if io_desc.io_type == 'Z':
            if io_desc.topo == 'distinct':
                raise Exception("Invalid norm for the given io_description!")
            if io_desc.topo == 'straight':
                return [abs(t-a) if type(a) is not list else io_desc.diff_calc(t, a) \
                        for t,a in zip(target, achieved)]
            if io_desc.topo == 'ring':
                range = io_desc.max - io_desc.min
                return [min(abs(t-a), abs(t-a+range), abs(t-a-range)) if type(a) is not list \
                     else io_desc.diff_calc(t, a) for t,a in zip(target, achieved)]
        if io_desc.io_type == 'Z':
            if io_desc.topo == 'straight':
                [abs(t-a) if type(a) is not list else io_desc.diff_calc(t, a) for t,a in zip(target, achieved)]
            if io_desc.topo == 'ring':
                range = io_desc.max - io_desc.min
                return [min(abs(t-a), abs(t-a+range), abs(t-a-range)) if type(a) is not list \
                     else io_desc.diff_calc(io_desc, t, a) for t,a in zip(target, achieved)]
        if io_desc.io_type == 'B':
            if io_desc.topo == 'hypercube':
                return [t^a if type(a) is not list else io_desc.diff_calc(t, a) for t, a in \
                 zip(target, achieved)]


    def default_norm(self, diff):
        '''
        :param diff(list): The diference of target and achieved values by Agent.
        :return: (io_desc.norm)th norm for diff vector.
        '''
        return sum([d**self.norm if type(d) is not list else self.norm_fn(d)**self.norm \
                for d in diff])**(1.0/self.norm)

    def zeroth_norm(self, diff):
        '''
        :param diff(list): The diference of target and achieved values by Agent.
        :return: (io_desc.norm)th norm for diff vector.
        '''
        return sum([d != 0 if type(d) is not list else self.norm_fn(d) for d in diff])

    def inf_norm(self, diff):
        '''
        :param diff(list): The diference of target and achieved values by Agent.
        :return: (io_desc.norm)th norm for diff vector.
        '''
        return max([d != 0 if type(d) is not list else self.norm_fn(d) for d in diff])

    def __str__(self, prefix = '', indent = '\t'):
        all_members = [a for a in dir(self) if not (a.startswith('__') and a.endswith('__')) and not callable(getattr(self, a))]
        total_indent = prefix + indent
        message = "******** IOdataype ********"  + '\n'
        for member in all_members:
            message += str(member) + ' = ' + str(self.__getattribute__(member)) + '\n'
        message = message[:-1]
        message = message.replace('\n', '\n'+total_indent)
        return message

    def __repr__(self):
        return self.__str__()

if __name__ == '__main__':
    normal_Z = IOdatatype('Z', io_topograph = 'ring', io_range_min = 0, io_range_max = 15, evaluation_norm = 2)
    diff = normal_Z.diff_calc([1,2,[3, 0]], [2,4,[6, 8]])
    norm = normal_Z.norm_fn(diff)
    print("diff = ", diff)
    print("norm = ", norm)
    pass