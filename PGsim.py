
import copy
from random import randint as randi

from IOdatatype import IOdatatype
from AgentWrapper import AgentCommonInformation, AgentAbstract, sample_Agent
from PGnetwork import PGnetwork

class PGsim:
    """
    Handles all function related to simulation.
    """
    def __init__(self, total_sim_count, network, common_agent_information, io_desc, verbose):
        """
        :type io_desc: IOdatatype.IOdatatype
        :type common_agent_information: AgentWrapper.AgentCommonInformation
        :type network: PGnetwork.PGnetwork
        """
        self.__total_sim_count = total_sim_count
        self.__total_steps_in_sim = common_agent_information.total_rounds_count
        self.curr_sim_count = 0
        self.curr_step_no = 0

        self.network = network
        self.common_agent_information = common_agent_information
        self.common_agent_information.reset_playground()
        self.io_desc = io_desc      # CAUTION: Repetetive information here. But io_desc cannot be accessed directly from
                                    # common_agent_information

        self.node_names = [node_value for node_value in self.network.nodes.keys()]
        self.all_output_logs = {node_value: [] for node_value in self.network.nodes.keys()}
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
            print(self.node_names)
        for self.curr_sim_count in range(self.__total_sim_count):
            output_all_this_sim = {node_value: [] for node_value in self.network.nodes.keys()}
            evaluation_incoming_vals_this_sim = {node_value: [] for node_value in self.network.nodes.keys()}
            for self.curr_step_no in range(self.__total_steps_in_sim):
                if verbose:
                    print("Sim No: ", self.curr_sim_count, "; Step No: ", self.curr_step_no)

                incoming_value_for_nodes = self.network.process_network(self.curr_step_no)
                output_all_nodes = self.network.enact_value()
                self.common_agent_information.take_a_sim_step()

                if self.curr_step_no >= self.common_agent_information.training_rounds_count:
                    for node_value, incoming_vals_this_step in incoming_value_for_nodes.items():
                        evaluation_incoming_vals_this_sim[node_value].append(incoming_vals_this_step)
                for node_value, output_this_step in output_all_nodes.items():
                    output_all_this_sim[node_value].append(output_this_step)
                if verbose:
                    print(output_all_nodes)
            self.network.reset_log()
            for node_value, output_this_sim in output_all_this_sim.items():
                self.all_output_logs[node_value].append(output_this_sim)
            for node_value, incoming_vals_this_sim in evaluation_incoming_vals_this_sim.items():
                self.evaluation_incoming_values_logs[node_value].append(incoming_vals_this_sim)
        if verbose:
            print("***************** End of Simulation *****************")

    def evaluate_performance(self, _targets):
        """
        :param _targets: The targets to be sent in following dict format:
            {
                node_value (for first Agent): [target_for_SIM_1, target_for_SIM_2 ...]
                node_value (for second Agent): target_for_al_SIM_rounds
                ...
            }
            The targets may be provided in a list if they differ across SIMs or a single value may be provided.
        :return:
        """
        targets_dict = copy.deepcopy(_targets)
        verbose = self.verbose
        if verbose:
            print("Evaluating performance for the following target values!")
            for node_value, target_list in targets_dict.items():
                print(node_value, ": ", target_list)
            print("Following is the IO description: ")
            print(self.io_desc)
        for node_value, sim_step_incoming_vals in self.evaluation_incoming_values_logs.items():
            print("Calculated norm for node = ", node_value)
            target_list = targets_dict[node_value]
            if type(target_list) is not list:
                target_list = [target_list]*self.__total_sim_count
            for step_incoming_vals, target in zip(sim_step_incoming_vals, target_list):
                diff_this_sim = self.io_desc.diff_calc(target, step_incoming_vals)
                norm_this_sim = self.io_desc.norm_fn(diff_this_sim)
                self.all_diffs[node_value].append(diff_this_sim)
                self.all_norms[node_value].append(norm_this_sim)
                print(norm_this_sim)
        return self.all_norms


if __name__ == '__main__':
    distinct_io = IOdatatype(io_type = 'Z', io_topograph = 'distinct', io_range_min = 1, io_range_max = 16, evaluation_norm = 0)
    distinct_setup = AgentCommonInformation(io_description = distinct_io, training_rounds = 15, evaluation_rounds = 10)
    AgentAbstract.Common_Data = distinct_setup
    nodes4_random_SC = {
        1: [2, 3],
        2: [3],
        3: [4],
        4: [1]
    }
    targets = {node: randi(distinct_io.min, distinct_io.max) for node in nodes4_random_SC}
    targets[4] = 16
    agents = [sample_Agent(target) for (target, _) in zip(targets, nodes4_random_SC)]
    PG1 = PGnetwork(nodes4_random_SC, agents)
    sim1 = PGsim(4, PG1, distinct_setup, distinct_io, True)
    sim1.run_sim()
    sim1.evaluate_performance(targets)

