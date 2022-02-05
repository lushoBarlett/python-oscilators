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

        for _ in range(self.parameters.oscilator_amount):
            self.displacements.append(0)
            self.mid_velocities.append(0)
            self.accelerations.append(0)

        for i in range(self.parameters.oscilator_amount):
            self.displacements[i] = self.displacement(i)

    def acceleration(self, i):
        return self.net_force(i) / self.parameters.oscilator_mass

    def net_force(self, i):
        return self.left_force(i) + self.right_force(i)

    def left_force(self, i):
        if self.is_first(i):
            return 0

        if self.is_last(i) and not self.parameters.last_open:
            return 0

        k = self.parameters.spring_constant
        return -k * (self.displacements[i] - self.displacements[i - 1])

    def right_force(self, i):
        if self.is_last(i):
            return 0

        if self.is_first(i) and not self.parameters.first_open:
            return 0

        k = self.parameters.spring_constant
        return -k * (self.displacements[i] - self.displacements[i + 1])

    def is_first(self, i):
        return i == 0

    def is_last(self, i):
        return i == len(self.positions) - 1

    def mid_velocity(self, i):
        if self.parameters.frame() == 1:
            return self.velocities[i] + self.accelerations[i] * self.parameters.dt() / 2

        return self.mid_velocities[i] + self.accelerations[i] * self.parameters.dt()

    def velocity(self, i):
        return self.mid_velocities[i] - self.accelerations[i] * self.parameters.dt() / 2

    def position(self, i):
        return self.positions[i] + self.mid_velocities[i] * self.parameters.dt()

    def displacement(self, i):
        return self.positions[i] - i * self.parameters.length_rest

    def update(self):
        for i in range(self.parameters.oscilator_amount):
            self.accelerations[i] = self.acceleration(i)
            self.mid_velocities[i] = self.mid_velocity(i)
            self.velocities[i] = self.velocity(i)
            self.positions[i] = self.position(i)
            self.displacements[i] = self.displacement(i)