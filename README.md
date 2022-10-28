# graph_MP_game

This is basically an arena to test AI/ML skills by developing Agents that compete among themselves or even humans. A Playground (PG) is a directed network where agents sit at a node. Each node has multiple input edges and multiple output edges in general. For each round of the game, all agents are assigned a target that they must try to receive in their input.
Gmae is divided into two sets. One for training and other for evaluation. All agent must provide an initial value that is passed along edge. In the second step the agents receive values from other agents through edge and based on these values that they receive and the their algorithm, they must through the output for second round.
This continues for the training period and then into evaluation period. Finally the scores are tallied for each agent based on some evaluation norm over their target and the values they received.

## File Description
### PGnetwork - A supportive class that helps in creation and management of graph/network.
### PGnode - A class to handle node and its operations. It has a member pointing to agent on the node.
### IOdatatype - A class to handle the datatype for input and output values of the Agent. Note that multiple types of data with diferent topographies are supported.
### AgentWrapper - A parent class for all agents. The agents must derive game related information through this class members.
