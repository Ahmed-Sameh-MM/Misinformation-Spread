from emotions import Emotions

# Parameters
α = 0.5  # Credibility of the hoax (0 ≤ α < 1)
β = 0.5  # Spreading rate of hoax/fact-checking
pv = 0.4  # Verification probability
pf = 0.1  # Forgetting probability

education = 1.0
emotions = Emotions(
    anger=0.5,
    trust=0.8,
)

# Graph Constants
NUM_AGENTS = 50  # Total number of agents
NUM_CONNECTIONS = 5  # Number of connections / agent
NUM_OF_INITIAL_BELIEVERS = round(NUM_AGENTS * 0.2)
NUM_STEPS = 10  # Number of simulation steps

# Plot Constants
FIG_SIZE = (11, 7)
