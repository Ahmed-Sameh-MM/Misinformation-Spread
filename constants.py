# Parameters
α = 0.5  # Credibility of the hoax (0 ≤ α < 1)
β = 0.5  # Spreading rate of hoax/fact-checking
pv = 0.4  # Verification probability
pf = 0.1  # Forgetting probability

# Graph Constants
NUM_AGENTS = 50  # Total number of agents
NUM_CONNECTIONS = 5  # Number of connections / agent
NUM_OF_INITIAL_BELIEVERS = round(NUM_AGENTS * 0.1)
NUM_STEPS = 10  # Number of simulation steps

# Plot Constants
FIG_SIZE = (11, 7)
