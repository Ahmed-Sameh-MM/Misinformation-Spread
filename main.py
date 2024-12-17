import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from agent_state import AgentState

# Parameters
α = 0.5  # Credibility of the hoax (0 ≤ α < 1)
β = 0.5  # Spreading rate of hoax/fact-checking
pv = 0.3  # Verification probability
pf = 0.1  # Forgetting probability
NUM_AGENTS = 50  # Total number of agents
NUM_STEPS = 10  # Number of simulation steps

# Initialize the network
social_network = nx.barabasi_albert_graph(NUM_AGENTS, 3)  # Barabasi-Albert social network
states = {node: AgentState.SUSCEPTIBLE for node in social_network.nodes()}  # Initial state: all Susceptible

# Seed the network with initial believers
initial_believers = np.random.choice(list(social_network.nodes()), size=10, replace=False)
for node in initial_believers:
    states[node] = AgentState.BELIEVER


# Function to count neighbors in a given state
def count_neighbors_in_state(node, state):
    return sum(1 for neighbor in social_network.neighbors(node) if states[neighbor] == state)

# Display basic graph info
print("Number of Agents:", social_network.number_of_nodes(), ',' ,end = ' ')
print("Number of Connections:", social_network.number_of_edges())

# Simulation loop
for step in range(NUM_STEPS):
    new_states = states.copy()  # To update states simultaneously

    for node in social_network.nodes():
        if states[node] == AgentState.SUSCEPTIBLE:  # Susceptible
            n_B = count_neighbors_in_state(node, AgentState.BELIEVER)
            n_FC = count_neighbors_in_state(node, AgentState.FACT_CHECKER)
            denom = n_B * (1 + α) + n_FC * (1 - α)

            # Compute probabilities of transitioning to B or FC
            f_B = β * (n_B * (1 + α)) / denom if denom > 0 else 0
            f_FC = β * (n_FC * (1 - α)) / denom if denom > 0 else 0

            # Decide state change
            rand = np.random.rand()
            if rand < f_B:
                new_states[node] = AgentState.BELIEVER
            elif rand < f_B + f_FC:
                new_states[node] = AgentState.FACT_CHECKER

        elif states[node] == AgentState.BELIEVER:  # Believer
            if np.random.rand() < pv:
                new_states[node] = AgentState.FACT_CHECKER  # Verify the hoax
            elif np.random.rand() < pf:
                new_states[node] = AgentState.SUSCEPTIBLE  # Forget and become Susceptible

        elif states[node] == AgentState.FACT_CHECKER:  # FactChecker
            if np.random.rand() < pf:
                new_states[node] = AgentState.SUSCEPTIBLE  # Forget and become Susceptible

    # Update states
    states = new_states.copy()

    # Visualization
    colors = {
        AgentState.SUSCEPTIBLE: "gray",
        AgentState.BELIEVER: "red",
        AgentState.FACT_CHECKER: "green",
    }
    node_colors = [colors[states[node]] for node in social_network.nodes()]

    nx.draw(social_network, node_color=node_colors, with_labels=False, node_size=50)
    plt.title(f"Step {step + 1}")
    plt.show()
