
import copy
from random import randint as randi
from pathlib import Path
import sys
import random
from colorama import Fore, Back, Style

current_dir = Path.cwd()
DG_dir = Path(current_dir / 'directed_graph')
if not current_dir in sys.path:
    sys.path.append(str(current_dir))
if not DG_dir in sys.path:
    sys.path.append(str(DG_dir))

from directed_graph import prime_DiGraph_Generator as pdgg
from directed_graph import extended_DiGraph as edg
from directed_graph import collection_DiGraph as cdg
from IOdatatype import IOdatatype
from AgentWrapper import AgentCommonInformation, AgentAbstract
from sampleAgents import target_returning_Agent, random_Agent, fixed_map_Agent
from PGnetwork import PGnetwork
from PGsim import PGsim
import memory_map


def find_period():
    MAPS_TO_TEST = 100
    INITIAL_CONDS_TO_TEST = 20
    MAX_ALLOWED_ROUNDS = 50000
    RANGES_TO_CHECK = [(1, 4)]#, (1, 7), (1, 11)]

    all_4nodes = cdg.load_object('directed_graph/all_5_nodes')
    MAIN_path_prefix = Path("5nodes_RE")
    unique_period_dict = dict()
    for index, DG in enumerate(all_4nodes.list_of_computed_DGs()):
        if index != 451:
            continue
        DG_nodes = DG.nodes()
        for a_range in RANGES_TO_CHECK:
            DG_level_path_prefix = MAIN_path_prefix/Path("index_" + str(index) + "_" + str(a_range[1]) + "elems")
            distinct_io = IOdatatype(io_type='Z', io_topograph='distinct', io_range_min=a_range[0], io_range_max=a_range[1], evaluation_norm=0)
            distinct_setup = AgentCommonInformation(io_description=distinct_io, training_rounds=int(0.8*MAX_ALLOWED_ROUNDS), evaluation_rounds=int(0.2*MAX_ALLOWED_ROUNDS))
            AgentAbstract.Common_Data = distinct_setup
            unique_period_for_given_DG_and_range = set()
            for experiment in range(MAPS_TO_TEST):
                print(Fore.BLACK + Back.GREEN + f"Checking for DG index = {index}; range = {a_range}; experiment no = {experiment}")
                print(Style.RESET_ALL)
                Experiment_level_path_prefix = DG_level_path_prefix/Path("exp_" + str(experiment))
                targets = {node: randi(distinct_io.min, distinct_io.max) for node in DG_nodes}
                MM_formats = memory_map.get_memory_map_format(DG)
                agents = [fixed_map_Agent(target, MM_formats[node]) for (target, node) in zip(targets, DG_nodes)]
                for agent, node in zip(agents, DG_nodes):
                    agent.my_name = node
                    agent.path_prefix = Experiment_level_path_prefix
                    agent.incoming_edges_count = DG.in_degree[node]
                    agent.reset_fix_map(save_map=True)
                PG1 = PGnetwork(DG.adj_, agents)
                sim = PGsim(INITIAL_CONDS_TO_TEST, PG1, distinct_setup, distinct_io, False)
                sim.path_prefix = Experiment_level_path_prefix
                sim.run_sim(save_log=True, early_break=True)
                # sim.evaluate_performance(targets)
                unique_period_for_given_DG_and_range = unique_period_for_given_DG_and_range.union(set(sim.repetition))
                with open(Experiment_level_path_prefix/Path('_individual_experiment_master.txt'), 'w') as f:
                    f.write(str(sim.repetition))
                    f.write("\n")
                    f.write(str(set(sim.repetition)))
                    f.write("\n")
                    unique_repetitions = list(set(sim.repetition))
                    for i in unique_repetitions:
                        f.write(f"Location for period = {i} is {sim.repetition.index(i)}\n")
            # End of Experiment for loop.
            with open(DG_level_path_prefix / Path('_DG_level_master.txt'), 'w') as f:
                f.write("List of all unique period found for: \n")
                f.write("Range = " + str(a_range)+"\n")
                f.write("and DG = " + str(DG)+"\n")
                f.write("is = " + str(unique_period_for_given_DG_and_range))
            unique_period_dict[(index, a_range[1])] = unique_period_for_given_DG_and_range
            with open(MAIN_path_prefix / Path("_master.txt"), 'w') as f:
                f.write("Printing the unique periods for all combinations.\n")
                for combo, periods in unique_period_dict.items():
                    f.write(str(combo) + ": \t" + str(periods) + "\n")
        # End of range for loop.
    #End of DG for loop.
    with open(MAIN_path_prefix/Path("_master.txt"), 'w') as f:
        f.write("Printing the unique periods for all combinations.\n")
        for combo, periods in unique_period_dict.items():
            f.write(str(combo) + ": \t" + str(periods) + "\n")


def MM_analysis(node_n, MMs_TO_TEST = 10, RANGES_TO_CHECK = None):
    if RANGES_TO_CHECK is None:
        RANGES_TO_CHECK = [(1, 4), (1, 7), (1, 11)]

    all_4nodes = cdg.load_object(f'directed_graph/all_{node_n}_nodes')
    MAIN_path_prefix = Path(f"MM_analysis_{node_n}nodes")
    MAIN_path_prefix.mkdir(parents=True, exist_ok=True)
    with open(MAIN_path_prefix / Path("_master.txt"), 'w') as f:
        f.write("Printing the max ring size for all combinations.\n")

    max_period_dict = dict()
    for index, DG in enumerate(all_4nodes.list_of_computed_DGs()):
        DG = DG.normalize()
        for a_range in RANGES_TO_CHECK:
            DG_level_path_prefix = MAIN_path_prefix/Path("index_" + str(index) + "_" + str(a_range[1]) + "elems")
            max_period_dict[(index, a_range[1])] = 0
            distinct_io = IOdatatype(io_type='Z', io_topograph='distinct', io_range_min=a_range[0], io_range_max=a_range[1], evaluation_norm=0)
            distinct_setup = AgentCommonInformation(io_description=distinct_io, training_rounds=int(4000), evaluation_rounds=int(1000))
            AgentAbstract.Common_Data = distinct_setup
            for experiment in range(MMs_TO_TEST):
                print(Fore.BLACK + Back.GREEN + f"Checking for DG index = {index}; range = {a_range}; experiment no = {experiment}", Style.RESET_ALL)
                targets = {node: randi(distinct_io.min, distinct_io.max) for node in DG.nodes}
                MM_formats = memory_map.get_memory_map_format(DG)
                agents = {node: fixed_map_Agent(targets[node], MM_formats[node]) for node in DG.nodes}
                for node, agent in agents.items():
                    agent.reset_fix_map(save_map=False)
                mm_Graph = memory_map.memoryMap_Graph(agents)
                try:
                    max_ring_size = len(mm_Graph.rings_formed[0])
                except IndexError:
                    max_ring_size = 0
                max_period_dict[(index, a_range[1])] = max(max_period_dict[(index, a_range[1])], max_ring_size)
                mm_Graph.save_MM_graph(path_prefix=DG_level_path_prefix)
                mm_Graph.save_MM_rings(path_prefix=DG_level_path_prefix)
            # End experiment for loop
            with open(MAIN_path_prefix / Path("_master.txt"), 'a') as f:
                f.write(f"({index}, {a_range[1]}): {max_period_dict[(index, a_range[1])]} \n")
        # End of range for loop
    #End of DG for loop

if __name__ == '__main__':
    # MM_analysis(4)
    find_period()