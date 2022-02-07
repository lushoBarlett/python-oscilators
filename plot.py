from matplotlib import pyplot

class Plot:
    
    def __init__(self):
        self.displacements = []
        self.velocities = []
        self.accelerations = []
        self.time = []

        self.total_energy = []
        self.kinetic_energy = []
        self.potential_energy = []

        self.errors = []
        self.dts = []

    def register_oscilator_state(self, displacement, velocity, acceleration, time):
        self.displacements.append(displacement)
        self.velocities.append(velocity)
        self.accelerations.append(acceleration)
        self.time.append(time)

    def kinematics(self, filename):
        fig, axes = pyplot.subplots(1, 3)

        axes[0].plot(self.time, self.displacements)
        axes[1].plot(self.time, self.velocities)
        axes[2].plot(self.time, self.accelerations)

        pyplot.savefig(filename)
        pyplot.close(fig)

    def register_energy(self, total, kinetic, potential):
        self.total_energy = total
        self.kinetic_energy = kinetic
        self.potential_energy = potential

    def energy(self, filename):
        fig, axes = pyplot.subplots(1, 3)

        axes[0].plot(self.time, self.total_energy)
        axes[1].plot(self.time, self.kinetic_energy)
        axes[2].plot(self.time, self.potential_energy)

        pyplot.savefig(filename)
        pyplot.close(fig)

    def register_relative_errors(self, errors, dts):
        self.errors = errors
        self.dts = dts

    def relative_errors(self, filename):
        fig, axis = pyplot.subplots(1, 1)

        axis.plot(self.dts, self.errors)

        pyplot.savefig(filename)
        pyplot.close(fig)