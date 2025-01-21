import random
from typing import List

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

from agent import Agent
from agent_socio_emotional_classes import *
from constants import *

# Function to count neighbours in a given state
def count_neighbors_in_state(agent: Agent, state: AgentState):
    return sum(1 for neighbour in social_network.neighbors(agent) if agents[neighbour.id].get_state() == state)

def draw_social_network_graph(agents:List[Agent], social_network, step: int):
    if SHOW_GRAPH:
        # Graph Visualization
        node_colors = [agent.node_color for agent in agents]

        pos = nx.spring_layout(social_network, seed=42)  # Layout for visualization

        plt.figure(figsize=FIG_SIZE)
        nx.draw(social_network, pos, node_color=node_colors, with_labels=True, node_size=300, font_size=8, edge_color="gray")
        plt.title(f"Step {step + 1}", fontsize=15)
        plt.show()

def plot_agent_states(susceptible: List[int], believers: List[int], fact_checkers: List[int]):
    simulation_steps = [step for step in range(NUM_STEPS + 1)]

    total = susceptible[-1] + believers[-1] + fact_checkers[-1]

    susceptible_percentage = f'Susceptible = {round(susceptible[-1] / total * 100, 3)}%'
    believers_percentage = f'Believers = {round(believers[-1] / total * 100, 3)}%'
    fact_checkers_percentage = f'Fact Checkers = {round(fact_checkers[-1] / total * 100, 3)}%'

    plt.figure(figsize=(10, 6))
    plt.plot(simulation_steps, susceptible, label=susceptible_percentage, color="gray", linestyle="--")
    plt.plot(simulation_steps, believers, label=believers_percentage, color="red", linestyle="-")
    plt.plot(simulation_steps, fact_checkers, label=fact_checkers_percentage, color="green", linestyle=":")

    plt.xlabel("Simulation Steps")
    plt.ylabel("Number of Agent States")
    plt.title(f"α={α}, High_Edu&Emo={SOCIO_EMOTIONAL_CLASSES_PERCENTAGES['HighEducationHighEmotional']}%, Low_Edu&Emo={SOCIO_EMOTIONAL_CLASSES_PERCENTAGES['LowEducationLowEmotional']}%, High_Edu_Low_Emo={SOCIO_EMOTIONAL_CLASSES_PERCENTAGES['HighEducationLowEmotional']}%, Low_Edu_High_Emo={SOCIO_EMOTIONAL_CLASSES_PERCENTAGES['LowEducationHighEmotional']}%")
    plt.legend()

    # Adding grid for better readability
    plt.grid(True, linestyle='--', alpha=0.7)

    # Show the plot
    plt.show()

def count_agent_states(agents: List[Agent]):
    susceptible = 0
    believers = 0
    fact_checkers = 0

    total = len(agents)

    for agent in agents:
        if agent.get_state() == AgentState.SUSCEPTIBLE:
            susceptible += 1

        elif agent.get_state() == AgentState.BELIEVER:
            believers += 1

        elif agent.get_state() == AgentState.FACT_CHECKER:
            fact_checkers += 1

    susceptible_percentage = f'{round(susceptible / total * 100, 2)}%'
    believers_percentage = f'{round(believers / total * 100, 2)}%'
    fact_checkers_percentage = f'{round(fact_checkers / total * 100, 2)}%'

    print(f'Susceptible: {susceptible_percentage} ({susceptible}), believers: {believers_percentage} ({believers}), fact_checkers: {fact_checkers_percentage} ({fact_checkers})')

    return susceptible, believers, fact_checkers

# Initialize the network
social_network = nx.Graph()

# Add NUM_PEOPLE as agents
agents = []


def generate_agents_by_percentage(percentages: dict):
    socio_emotional_classes = [
        HighEducationHighEmotional(),
        LowEducationLowEmotional(),
        HighEducationLowEmotional(),
        LowEducationHighEmotional(),
    ]

    isRandom = True

    for key, value in percentages.items():
        if value != 0:
            isRandom = False
            break

    if isRandom:
        for i in range(NUM_AGENTS):
            chosen_socio_emotional_class = random.choice(socio_emotional_classes)

            agents.append(Agent(
                id=i,
                socio_emotional_class=chosen_socio_emotional_class,
            ))

    else:
        # Normalize the percentages
        normalized_percentages = {k: v / 100 for k, v in percentages.items()}

        # Calculate the number of agents per class
        class_counts = {k: int(v * NUM_AGENTS) for k, v in normalized_percentages.items()}

        # Adjust for rounding errors to ensure total agents equal NUM_AGENTS
        remaining_agents = NUM_AGENTS - sum(class_counts.values())

        for _ in range(remaining_agents):
            random_class = random.choice(list(class_counts.keys()))
            class_counts[random_class] += 1

        # Generate agents
        id_counter = 0

        for class_name, count in class_counts.items():
            socio_emotional_class = globals()[class_name]()

            for _ in range(count):
                agents.append(Agent(
                    id=id_counter,
                    socio_emotional_class=socio_emotional_class,
                ))
                id_counter += 1

generate_agents_by_percentage(SOCIO_EMOTIONAL_CLASSES_PERCENTAGES)

social_network.add_nodes_from(agents)

# Add random edges to simulate connections between agents, assuming that each agent has NUM_CONNECTIONS connections
for agent in agents:
    connections = random.sample(agents, NUM_CONNECTIONS)

    for connection in connections:
        if agent != connection:  # Avoid self-loops
            social_network.add_edge(agent, connection)

# Seed the network with initial believers
initial_believers = np.random.choice(agents, size=NUM_OF_INITIAL_BELIEVERS, replace=False)

for believer in initial_believers:
    agents[believer.id].set_state(AgentState.BELIEVER)

if ADD_FACT_CHECKERS:
    # Ensure that we have exactly 10% fact_checkers
    # Exclude initial believers from the list of potential fact_checkers
    non_believers = [agent for agent in agents if agent not in initial_believers]

    # Seed the network with initial fact-checkers
    initial_fact_checkers = np.random.choice(non_believers, size=NUM_OF_INITIAL_BELIEVERS, replace=False)

    for fact_checker in initial_fact_checkers:
        agents[fact_checker.id].set_state(AgentState.FACT_CHECKER)

# Display basic graph info
print("Number of Agents:", social_network.number_of_nodes(), ',' ,end = ' ')
print("Number of Connections:", social_network.number_of_edges(), '\n')

s, b, fc = count_agent_states(agents)

susceptible = [s]
believers = [b]
fact_checkers = [fc]

# Simulation loop
for step in range(NUM_STEPS):
    updated_agents = agents.copy() # To update agent states simultaneously

    s_to_b_count = 0
    s_to_fc_count = 0
    b_to_fc_count = 0

    for index, agent in enumerate(agents):
        # Simulating the agent's anger, education, and trust parameters
        agent_anger = agent.socio_emotional_class.anger
        agent_education = agent.socio_emotional_class.education
        agent_trust = agent.socio_emotional_class.trust

        if agent.get_state() == AgentState.SUSCEPTIBLE:  # Susceptible
            n_B = count_neighbors_in_state(agent, AgentState.BELIEVER)
            n_FC = count_neighbors_in_state(agent, AgentState.FACT_CHECKER)
            n_total = n_B + n_FC

            numerator_B = n_B * (1 + α)
            numerator_FC = n_FC * (1 - α)
            denom = numerator_B + numerator_FC

            # Compute probabilities of transitioning to B or FC
            f_B = β * numerator_B / denom if denom > 0 else 0
            f_FC = β * numerator_FC / denom if denom > 0 else 0

            believer_trust = agent_trust
            believer_trust *= (n_B / n_total) if n_total > 0 else 0

            fact_checker_trust = agent_trust
            fact_checker_trust *= (n_FC / n_total) if n_total > 0 else 0

            f_B *= (1 + agent_anger - agent_education + believer_trust)
            f_FC *= (1 - agent_anger + agent_education + fact_checker_trust)

            # After adjustments, normalize f_B & f_FC, to ensure their sum doesn't exceed 1:
            total = f_B + f_FC

            if total > 1:
                f_B /= total
                f_FC /= total

            temp_rand = np.random.rand()

            # Decide state change
            if temp_rand < f_B and f_B >= f_FC:
                updated_agents[index].set_state(AgentState.BELIEVER)
                s_to_b_count += 1

            elif temp_rand < f_FC:
                updated_agents[index].set_state(AgentState.FACT_CHECKER)
                s_to_fc_count += 1

        elif agent.get_state() == AgentState.BELIEVER:  # Believer
            n_B = count_neighbors_in_state(agent, AgentState.BELIEVER)
            n_FC = count_neighbors_in_state(agent, AgentState.FACT_CHECKER)
            n_total = n_B + n_FC

            pv = agent_education - agent_anger # Verification probability

            pv += (1 - α) * (agent_trust * (n_FC - n_B)) / n_total

            pv = pv if pv > 0 else 0

            if np.random.rand() < pv:
                updated_agents[index].set_state(AgentState.FACT_CHECKER)  # Verify the hoax
                b_to_fc_count += 1

            elif np.random.rand() < pf:
                updated_agents[index].set_state(AgentState.SUSCEPTIBLE)  # Forget and become Susceptible

        elif agent.get_state() == AgentState.FACT_CHECKER:  # FactChecker
            if np.random.rand() < pf:
                updated_agents[index].set_state(AgentState.SUSCEPTIBLE)  # Forget and become Susceptible

    print(f's -> b: {s_to_b_count}, s -> fc: {s_to_fc_count}, b -> fc: {b_to_fc_count}\n')

    # Update the states of the agents
    agents = updated_agents.copy()

    draw_social_network_graph(agents, social_network, step)

    s, b, fc = count_agent_states(agents)

    susceptible.append(s)
    believers.append(b)
    fact_checkers.append(fc)

plot_agent_states(susceptible, believers, fact_checkers)
