
import copy
from random import randint as randi
from pathlib import Path
import sys
import random

current_dir = Path.cwd()
DG_dir = Path(current_dir / 'directed_graph')
if not current_dir in sys.path:
    sys.path.append(str(current_dir))
if not DG_dir in sys.path:
    sys.path.append(str(DG_dir))

from directed_graph import prime_DiGraph_Generator as pdgg
from IOdatatype import IOdatatype
from AgentWrapper import AgentCommonInformation, AgentAbstract
from sampleAgents import target_returning_Agent, random_Agent, fixed_map_Agent
from PGnetwork import PGnetwork
from PGsim import PGsim

if __name__ == '__main__':
    all_primes_10 = pdgg.primeDiGraphGenerator('using_isomorphic_hash', path_prefix='directed_graph')
    _4node_primes = all_primes_10.cdg.list_of_computed_DGs(4)
    ring_4nodes = _4node_primes[3]
    ring_4nodes_nodes = ring_4nodes.nodes()

    distinct_io = IOdatatype(io_type='Z', io_topograph='distinct', io_range_min=1, io_range_max=4, evaluation_norm=0)
    distinct_setup = AgentCommonInformation(io_description=distinct_io, training_rounds=4000, evaluation_rounds=1000)
    AgentAbstract.Common_Data = distinct_setup
    targets = {node: randi(distinct_io.min, distinct_io.max) for node in ring_4nodes_nodes}
    agents = [fixed_map_Agent(target) for (target, _) in zip(targets, ring_4nodes_nodes)]
    [agent.set_name(node) for agent, node in zip(agents, ring_4nodes_nodes)]
    PG1 = PGnetwork(ring_4nodes.adj_, agents)
    sim1 = PGsim(20, PG1, distinct_setup, distinct_io, False)
    sim1.run_sim()
    sim1.evaluate_performance(targets)
    sim1.save_log()
