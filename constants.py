# Parameters
from agent_state import AgentState

α = 0.8  # Credibility of the hoax (0 ≤ α < 1)
β = 0.5  # Spreading rate of hoax/fact-checking
pf = 0.2  # Forgetting probability

# Graph Constants
NUM_AGENTS = 500  # Total number of agents
NUM_CONNECTIONS = round(NUM_AGENTS * 0.1)  # Number of connections / agent
NUM_OF_INITIAL_BELIEVERS = round(NUM_AGENTS * 0.1)
NUM_STEPS = 200  # Number of simulation steps

SOCIO_EMOTIONAL_CLASSES_PERCENTAGES = {
    "HighEducationLowEmotional": 77,
    "LowEducationHighEmotional": 10,

    "LowEducationLowEmotional": 6,
    "HighEducationHighEmotional": 7,
}

ADD_FACT_CHECKERS = False

SHOW_GRAPH = False

# Plot Constants
FIG_SIZE = (11, 7)

node_colors = {
    AgentState.SUSCEPTIBLE: "grey",
    AgentState.BELIEVER: "red",
    AgentState.FACT_CHECKER: "green",
}
