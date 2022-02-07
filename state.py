from copy import deepcopy
import json


class State:

    def from_file(filename, parameters):
        with open(filename, "r") as state:
            unparsed_state = state.read()
            parsed_state = json.loads(unparsed_state)
            return State(parsed_state, parameters)

    def __init__(self, state, parameters):
        self.positions = state["x"]
        self.velocities = state["v"]
        self.parameters = parameters

        self.displacements = []
        self.mid_velocities = []
        self.accelerations = []

        self.elapsed_time = 0

        for _ in range(self.parameters.oscilator_amount):
            self.displacements.append(0)
            self.mid_velocities.append(0)
            self.accelerations.append(0)

        for i in range(self.parameters.oscilator_amount):
            self.displacements[i] = self.positions[i] - i * self.parameters.rest_length

    def left_force(self, i):
        if i == 0:
            return 0

        if i == self.parameters.oscilator_amount - 1 and not self.parameters.last_open:
            return 0

        k = self.parameters.spring_constant
        return -k * (self.displacements[i] - self.displacements[i - 1])

    def right_force(self, i):
        if i == self.parameters.oscilator_amount - 1:
            return 0

        if i == 0 and not self.parameters.first_open:
            return 0

        k = self.parameters.spring_constant
        return -k * (self.displacements[i] - self.displacements[i + 1])

    def update(self):
        dt = self.parameters.dt()

        for i in range(self.parameters.oscilator_amount):
            self.accelerations[i] = (self.left_force(i) + self.right_force(i)) / self.parameters.oscilator_mass

            if self.parameters.frame() == 1:
                self.mid_velocities[i] = self.velocities[i] + self.accelerations[i] * dt / 2
            else:
                self.mid_velocities[i] += + self.accelerations[i] * dt

            self.velocities[i] = self.mid_velocities[i] - self.accelerations[i] * dt / 2

            self.positions[i] += self.mid_velocities[i] * self.parameters.dt()

            self.displacements[i] = self.positions[i] - i * self.parameters.rest_length

            self.elapsed_time += dt

    def current_displacements(self):
        return deepcopy(self.displacements)

    def current_velocities(self):
        return deepcopy(self.velocities)

    def current_accelerations(self):
        return deepcopy(self.accelerations)

    def current_time(self):
        return self.elapsed_time