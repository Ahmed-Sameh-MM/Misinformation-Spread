from agent_state import AgentState
from agent_socio_emotional_classes import AgentSocioEmotionalClasses

node_colors = {
    AgentState.SUSCEPTIBLE: "gray",
    AgentState.BELIEVER: "red",
    AgentState.FACT_CHECKER: "green",
}

class Agent:
    def __init__(self, id: int, socio_emotional_class: AgentSocioEmotionalClasses, state: AgentState=AgentState.SUSCEPTIBLE):
        self.id = id
        self.name = f'A{id + 1}'

        # {Initial state: Susceptible}
        self._state = state
        self.node_color = node_colors[self._state]

        self.socio_emotional_class = socio_emotional_class

    def get_state(self):
        return self._state

    def set_state(self, new_state: AgentState):
        self._state = new_state
        self.node_color = node_colors[self._state]

    def to_string(self):
        return f'id: {self.id}, name: {self.name}, state: {self._state}, node color: {self.node_color}, socio emotional class: {self.socio_emotional_class}'

    def __str__(self):
        return self.name
