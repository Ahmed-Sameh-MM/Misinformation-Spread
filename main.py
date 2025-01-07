import random
from typing import List

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

from agent import Agent
from agent_state import AgentState
from agent_socio_emotional_classes import *
from constants import *

def draw_social_network_graph(agents:List[Agent], social_network, step: int):
    if SHOW_GRAPH:
        # Graph Visualization
        node_colors = [agent.node_color for agent in agents]

        pos = nx.spring_layout(social_network, seed=42)  # Layout for visualization

        plt.figure(figsize=FIG_SIZE)
        nx.draw(social_network, pos, node_color=node_colors, with_labels=True, node_size=300, font_size=8, edge_color="gray")
        plt.title(f"Step {step + 1}", fontsize=15)
        plt.show()

def print_agent_states(agents: List[Agent]):
    susceptible = 0
    believers = 0
    fact_checkers = 0

    for agent in agents:
        if agent.get_state() == AgentState.SUSCEPTIBLE:
            susceptible += 1

        elif agent.get_state() == AgentState.BELIEVER:
            believers += 1

        elif agent.get_state() == AgentState.FACT_CHECKER:
            fact_checkers += 1

    print(f'Susceptible: {susceptible}, believers: {believers}, fact_checkers: {fact_checkers}')

# Initialize the network
# social_network = nx.barabasi_albert_graph(NUM_AGENTS, 3)
social_network = nx.Graph()

# print(social_network.nodes())

# Add NUM_PEOPLE as agents
agents = []

for i in range(NUM_AGENTS):
    chosen_socio_emotional_class = random.choice([HighEducationHighEmotional, LowEducationLowEmotional, HighEducationLowEmotional, LowEducationHighEmotional])

    agents.append(Agent(
        id=i,
        socio_emotional_class=chosen_socio_emotional_class(),
    ))

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

    for index, agent in enumerate(agents):
        # Simulating the agent's anger, education, and trust parameters
        agent_anger = agent.socio_emotional_class.anger
        agent_education = agent.socio_emotional_class.education
        agent_trust = agent.socio_emotional_class.trust

        if agent.get_state() == AgentState.SUSCEPTIBLE:  # Susceptible
            n_B = count_neighbors_in_state(agent, AgentState.BELIEVER)
            n_FC = count_neighbors_in_state(agent, AgentState.FACT_CHECKER)

            numerator_B = n_B * (1 + α)
            numerator_FC = n_FC * (1 - α)
            denom = numerator_B + numerator_FC

            # Compute probabilities of transitioning to B or FC
            f_B = β * numerator_B / denom if denom > 0 else 0
            f_FC = β * numerator_FC / denom if denom > 0 else 0

            # Modify the probabilities based on the majority state of neighbors
            if n_B > n_FC:
                f_B *= (1 + agent_anger - agent_education + agent_trust)
                f_FC *= (1 - agent_anger + agent_education - agent_trust)

            elif n_FC > n_B:
                f_B *= (1 + agent_anger - agent_education - agent_trust)
                f_FC *= (1 - agent_anger + agent_education + agent_trust)

            else: # Equal numbers of Believers and FactCheckers
                pass

            # After adjustments, normalize f_B & f_FC, to ensure their sum doesn't exceed 1:
            total = f_B + f_FC

            if total > 1:
                f_B /= total
                f_FC /= total

            # Decide state change
            if np.random.rand() < f_B:
                updated_agents[index].set_state(AgentState.BELIEVER)

            elif np.random.rand() < f_FC: # TODO check this transition to be correct or not
                updated_agents[index].set_state(AgentState.FACT_CHECKER)

        elif agent.get_state() == AgentState.BELIEVER:  # Believer
            n_B = count_neighbors_in_state(agent, AgentState.BELIEVER)
            n_FC = count_neighbors_in_state(agent, AgentState.FACT_CHECKER)

            pv = None # Verification probability

            # Modify the probabilities based on the majority state of neighbors
            if n_B > n_FC:
                pv = agent_education - agent_anger - agent_trust

            elif n_FC > n_B:
                pv = agent_education - agent_anger + agent_trust

            else:  # Equal numbers of Believers and FactCheckers
                pv = agent_education - agent_anger

            pv = pv if pv > 0 else 0

            if np.random.rand() < pv:
                updated_agents[index].set_state(AgentState.FACT_CHECKER)  # Verify the hoax

            elif np.random.rand() < pf:
                updated_agents[index].set_state(AgentState.SUSCEPTIBLE)  # Forget and become Susceptible

        elif agent.get_state() == AgentState.FACT_CHECKER:  # FactChecker
            if np.random.rand() < pf:
                updated_agents[index].set_state(AgentState.SUSCEPTIBLE)  # Forget and become Susceptible

    # Update the states of the agents
    agents = updated_agents.copy()

    draw_social_network_graph(agents, social_network, step)

    print_agent_states(agents)
