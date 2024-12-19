import random

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

from agent import Agent
from agent_state import AgentState
from constants import *

# social_network = nx.barabasi_albert_graph(NUM_AGENTS, 3)

# Initialize the network
social_network = nx.Graph()

# Add NUM_PEOPLE as agents
agents = [Agent(id=(i - 1), name=f'A{i}') for i in range(1, NUM_AGENTS + 1)]
social_network.add_nodes_from(agents)

# Add random edges to simulate friendships
# Assuming each agent has 1-NUM_FRIENDS random connections
for agent in agents:
    num_connections = random.randint(1, NUM_CONNECTIONS + 1)
    connections = random.sample(agents, num_connections)

    for connection in connections:
        if agent != connection:  # Avoid self-loops
            social_network.add_edge(agent, connection)

# Seed the network with initial believers
initial_believers = np.random.choice(list(agents), size=NUM_OF_INITIAL_BELIEVERS, replace=False)

for believer in initial_believers:
    agents[believer.id].set_state(AgentState.BELIEVER)

# Function to count neighbours in a given state
def count_neighbors_in_state(agent: Agent, state: AgentState):
    return sum(1 for neighbour in social_network.neighbors(agent) if agents[neighbour.id].get_state() == state)

# Display basic graph info
print("Number of Agents:", social_network.number_of_nodes(), ',' ,end = ' ')
print("Number of Connections:", social_network.number_of_edges())

# Simulation loop
for step in range(NUM_STEPS):
    updated_agents = agents.copy() # To update agent states simultaneously

    for agent in agents:
        agent_id = agent.id

        if agents[agent_id].get_state() == AgentState.SUSCEPTIBLE:  # Susceptible
            n_B = count_neighbors_in_state(agent, AgentState.BELIEVER)
            n_FC = count_neighbors_in_state(agent, AgentState.FACT_CHECKER)
            denom = n_B * (1 + α) + n_FC * (1 - α)

            # Compute probabilities of transitioning to B or FC
            f_B = β * (n_B * (1 + α)) / denom if denom > 0 else 0
            f_FC = β * (n_FC * (1 - α)) / denom if denom > 0 else 0

            # Decide state change
            rand = np.random.rand()

            if rand < f_B:
                updated_agents[agent_id].set_state(AgentState.BELIEVER)

            elif rand < f_B + f_FC:
                updated_agents[agent_id].set_state(AgentState.FACT_CHECKER)

        elif agents[agent_id].get_state() == AgentState.BELIEVER:  # Believer
            if np.random.rand() < pv:
                updated_agents[agent_id].set_state(AgentState.FACT_CHECKER)  # Verify the hoax

            elif np.random.rand() < pf:
                updated_agents[agent_id].set_state(AgentState.SUSCEPTIBLE)  # Forget and become Susceptible

        elif agents[agent_id].get_state() == AgentState.FACT_CHECKER:  # FactChecker
            if np.random.rand() < pf:
                updated_agents[agent_id].set_state(AgentState.SUSCEPTIBLE)  # Forget and become Susceptible

    # Update the states of the agents
    agents = updated_agents.copy()

    # Graph Visualization
    node_colors = [agent.node_color for agent in agents]

    pos = nx.spring_layout(social_network, seed=42)  # Layout for visualization

    plt.figure(figsize=FIG_SIZE)
    nx.draw(social_network, pos, node_color=node_colors, with_labels=True, node_size=300, font_size=8, edge_color="gray")
    plt.title(f"Step {step + 1}", fontsize=15)
    plt.show()
