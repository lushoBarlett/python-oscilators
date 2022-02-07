from copy import deepcopy


class State:

    def __init__(self, state, parameters):
        self.positions = state["x"]
        self.velocities = state["v"]
        self.parameters = parameters

        self.displacements = []
        self.mid_velocities = []
        self.accelerations = []

        self.elapsed_time = 0

        for _ in range(self.parameters['osc_num']):
            self.displacements.append(0)
            self.mid_velocities.append(0)
            self.accelerations.append(0)

        for i in range(self.parameters['osc_num']):
            self.displacements[i] = self.positions[i] - i * self.parameters['l_rest']

    def left_force(self, i):
        if i == 0:
            return 0

        if i == self.parameters['osc_num'] - 1 and not self.parameters['last_is_open']:
            return 0

        k = self.parameters['k']
        return -k * (self.displacements[i] - self.displacements[i - 1])

    def right_force(self, i):
        if i == self.parameters['osc_num'] - 1:
            return 0

        if i == 0 and not self.parameters['first_is_open']:
            return 0

        k = self.parameters['k']
        return -k * (self.displacements[i] - self.displacements[i + 1])

    def update(self):
        dt = self.parameters['dt'][self.parameters['simulation'] - 1]

        for i in range(self.parameters['osc_num']):
            self.accelerations[i] = (self.left_force(i) + self.right_force(i)) / self.parameters['mass']

            if self.parameters['frame'] == 1:
                self.mid_velocities[i] = self.velocities[i] + self.accelerations[i] * dt / 2
            else:
                self.mid_velocities[i] += + self.accelerations[i] * dt

            self.velocities[i] = self.mid_velocities[i] - self.accelerations[i] * dt / 2

            self.positions[i] += self.mid_velocities[i] * dt

            self.displacements[i] = self.positions[i] - i * self.parameters['l_rest']

            self.elapsed_time += dt

    def current_displacements(self):
        return deepcopy(self.displacements)

    def current_velocities(self):
        return deepcopy(self.velocities)

    def current_accelerations(self):
        return deepcopy(self.accelerations)

    def current_time(self):
        return self.elapsed_time