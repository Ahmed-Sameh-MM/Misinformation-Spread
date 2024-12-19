from agent_state import AgentState

node_colors = {
    AgentState.SUSCEPTIBLE: "gray",
    AgentState.BELIEVER: "red",
    AgentState.FACT_CHECKER: "green",
}

class Agent:
    def __init__(self, id: int, name: str, state: AgentState=AgentState.SUSCEPTIBLE):
        self.id = id
        self.name = name

        # {Initial state: Susceptible}
        self._state = state
        self.node_color = node_colors[self._state]

    def get_state(self):
        return self._state

    def set_state(self, new_state: AgentState):
        self._state = new_state
        self.node_color = node_colors[self._state]

    def to_string(self):
        return f'id: {self.id}, name: {self.name}, state: {self._state}, node color: {self.node_color}'

    def __str__(self):
        return self.name
