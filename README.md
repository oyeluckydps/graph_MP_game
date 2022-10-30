# graph_MP_game

This is basically an arena to test AI/ML skills by developing Agents that compete among themselves or even humans. A Playground (PG) is a directed network where agents sit at a node. Each node has multiple input edges and multiple output edges in general. For each round of the game, all agents are assigned a target that they must try to receive in their input.
Gmae is divided into two sets. One for training and other for evaluation. All agent must provide an initial value that is passed along edge. In the second step the agents receive values from other agents through edge and based on these values that they receive and the their algorithm, they must through the output for second round.
This continues for the training period and then into evaluation period. Finally the scores are tallied for each agent based on some evaluation norm over their target and the values they received.

## File Description
### PGnetwork
A supportive class that helps in creation and management of graph/network.
### PGnode 
A class to handle node and its operations. It has a member pointing to agent on the node.
### IOdatatype
A class to handle the datatype for input and output values of the Agent. Note that multiple types of data with diferent topographies are supported.
### AgentWrapper
- AgentCommonInformation:
A parent class to aggregate all the common information that is to be sahred with an Agent. Various properties are set and they are expected to be used but none of the data members are expected to be overwritten. SO, ALL MEMBERS are READ only. To make it strict we might have to add some protection.
- AgentAbstract:
An Abstract class that has a member Common_Data which contains all the common information. It also puts th blueprint for the Agent implementation.
- sample_Agent:
A sample agent to explain how agent implementation is expected.
### PGsim
A class to handle all simulation steps and evaluation releated functions on the Playground.
