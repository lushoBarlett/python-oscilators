import json


class State:
    def from_file(filename):
        with open(filename, "r") as state:
            unparsed_state = state.read()
            parsed_state = json.loads(unparsed_state)
            return State(parsed_state)


    def __init__(self, state):
        self.positions = state["x"]
        self.velocities = state["v"]