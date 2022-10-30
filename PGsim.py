import copy

class PGsim:
    '''
    Handles all function related to simulation.
    '''
    def __init__(self, total_sim_count, network, commonAgentInformation, IO_desc, verbose):
        """
        :type IO_desc: IOdatatype.IOdatatype
        :type commonAgentInformation: AgentWrapper.AgentCommonInformation
        :type network: PGnetwork.PGnetwork
        """
        self.__total_sim_count = total_sim_count
        self.__total_steps_in_sim = commonAgentInformation.total_rounds_count
        self.curr_sim_count = 0
        self.curr_step_no = 0

        self.network = network
        self.commonAgentInformation = commonAgentInformation
        self.commonAgentInformation.reset_playground()
        self.IO_desc = IO_desc      # CAUTION: Repetetive information here. But IO_desc cannot be accessed directly from
                                    # commonAgentInformation

        self.all_output_logs = {node_value:[] for node_value in self.network.nodes.keys()}
        self.evaluation_incoming_values_logs = {node_value: [] for node_value in self.network.nodes.keys()}
        self.all_diffs = {node_value: [] for node_value in self.network.nodes.keys()}
        self.all_norms = {node_value: [] for node_value in self.network.nodes.keys()}

        self.verbose = verbose

    def run_sim(self):
        verbose = self.verbose
        if verbose:
            print("Starting the simulation with following configuration.")
            print(self)
            print("*****************************************************")
            print("Printing node values:")
            print(self.all_output_logs['node_names'])
        for self.curr_sim_count in range(self.__total_sim_count):
            output_all_this_sim = {node_value: [] for node_value in self.network.nodes.keys()}
            evaluation_incoming_vals_this_sim = {node_value: [] for node_value in self.network.nodes.keys()}
            for self.curr_step_no in range(self.__total_steps_in_sim):
                if verbose:
                    print("Sim No: ", self.curr_sim_count, "; Step No: ", self.curr_step_no)

                incoming_value_for_nodes = self.network.process_network()
                output_all_nodes = self.network.enact_value()
                self.commonAgentInformation.take_a_sim_step()

                if self.curr_step_no >= self.commonAgentInformation.training_rounds_count:
                    for node_value, incoming_vals_this_step in incoming_value_for_nodes:
                        evaluation_incoming_vals_this_sim[node_value].append(incoming_vals_this_step)
                for node_value, output_this_step in output_all_nodes:
                    output_all_this_sim[node_value].append(output_this_step)
                if verbose:
                    print(output_all_nodes)
            self.network.reset_log()
            for node_value, output_this_sim in output_all_this_sim:
                self.all_output_logs[node_value].append(output_this_sim)
            for node_value, incoming_vals_this_sim in evaluation_incoming_vals_this_sim:
                self.evaluation_incoming_values_logs[node_value].append(incoming_vals_this_sim)
        if verbose:
            print("***************** End of Simulation *****************")


    def evaluate_performance(self, _targets):
        '''
        :param targets: The targets to be sent in following dict format:
            {
                node_value (for first Agent): [target_for_SIM_1, target_for_SIM_2 ...]
                node_value (for second Agent): target_for_al_SIM_rounds
                ...
            }
            The targets may be provided in a list if they differ across SIMs or a single value may be provided.
        :return:
        '''
        targets_dict = copy.deepcopy(_targets)
        verbose = self.verbose
        if verbose:
            print("Evaluating performance for the following target values!")
            for node_value, target_list in targets_dict.values():
                print(node_value, ": ", target_list)
            print("Following is the IO description: ")
            print(self.IO_desc)
        for node_value, sim_step_incoming_vals in self.evaluation_incoming_values_logs.values():
            print("Calculated norm for node = ", node_value)
            target_list = targets_dict[node_value]
            if type(target_list) is not list:
                target_list = [target_list]*self.__total_sim_count
            for step_incoming_vals, target in zip(sim_step_incoming_vals, target_list):
                diff_this_sim = self.IO_desc.diff_calc(target, step_incoming_vals)
                norm_this_sim = self.IO_desc.norm_fn(diff_this_sim)
                self.all_diffs[node_value].append(diff_this_sim)
                self.all_norms[node_value].append(norm_this_sim)
                print(norm_this_sim)
        return self.all_norms


