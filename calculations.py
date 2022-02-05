from dis import dis
import math
from statistics import median_grouped
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

            for i in range(self.parameters.oscilator_amount):
                kinetic[t] += velocities[i] ** 2

            kinetic[t] *= self.parameters.oscilator_mass / 2
        
        return kinetic

    def calc_potential(self):
        potential = []

        for t, displacements in enumerate(self.dx):

            potential.append(0)

            for i in range(self.parameters.oscilator_amount - 1):
                potential[t] += (displacements[i + 1] - displacements[i]) ** 2

            potential[t] *= self.parameters.spring_constant / 2
        
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
            middle_oscilator_index = int(len(displacements) / 2)
            middle_oscilator_displacements.append(displacements[middle_oscilator_index])

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

        return 2 * math.pi / mean_period