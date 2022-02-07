from math import pi, sqrt
from scipy import signal


class Calculations:

    def __init__(self, parameters):
        self.parameters = parameters

        self.dx = []
        self.v = []
        self.t = []

    def register_displacements_and_velocities(self, displacements, velocities, time):
        self.dx.append(displacements)
        self.v.append(velocities)
        self.t.append(time)

    def calc_kinetic(self):
        kinetic = []

        for t, velocities in enumerate(self.v):

            kinetic.append(0)

            for i in range(self.parameters['osc_num']):
                kinetic[t] += velocities[i] ** 2

            kinetic[t] *= self.parameters['mass'] / 2
        
        return kinetic

    def calc_potential(self):
        potential = []

        for t, displacements in enumerate(self.dx):

            potential.append(0)

            for i in range(self.parameters['osc_num'] - 1):
                potential[t] += (displacements[i + 1] - displacements[i]) ** 2

            potential[t] *= self.parameters['k'] / 2
        
        return potential

    def calc_E(self):
        kinetic = self.calc_kinetic()
        potential = self.calc_potential()

        total = []
        for k, p in zip(kinetic, potential):
            total.append(k + p)

        return (total, kinetic, potential)

    def mean_frequency(self):
        middle_oscilator_displacements = []

        for displacements in self.dx:
            middle = int(self.parameters['osc_num'] / 2)
            middle_oscilator_displacements.append(displacements[middle])

        indices, _ = signal.find_peaks(middle_oscilator_displacements)

        period_approximates = []

        for i in range(len(indices) - 1):
            tmax1 = self.t[indices[i]]
            tmax2 = self.t[indices[i + 1]]
            period_approximates.append(abs(tmax1 - tmax2))

        mean_period = 0

        for p in period_approximates:
            mean_period += p

        mean_period /= len(period_approximates)

        if mean_period == 0:
            return None

        return 2 * pi / mean_period

    def calc_wave_vel(self):
        last_oscilator_velocities = []

        for velocities in self.v:
            last_oscilator_velocity = velocities[len(velocities) - 1]
            last_oscilator_velocities.append(last_oscilator_velocity)

        time_of_movement = 0
        for t, v in zip(self.t, velocities):
            time_of_movement = t
            if v > 0:
                break

        spring_amount = self.parameters['osc_num'] - 1
        length_of_rest = self.parameters['l_rest'] * spring_amount

        return length_of_rest / time_of_movement

    def calc_wave_vel_analitic(self):
        k = self.parameters['k']
        m = self.parameters['mass']
        l = self.parameters['l_rest']
        return sqrt(k / m) * l

    def relative_error(real, approx):
        return abs(real - approx) / real