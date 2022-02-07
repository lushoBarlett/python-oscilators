import os

from calculations import Calculations
from parameters import Parameters
from plot import Plot
from state import State


def write_numbers(filename, numbers):

    def map_str(sequence):
        result = []
        for element in sequence:
            result.append(str(element))
        return result

    first_written_line = not os.path.exists(filename)

    with open(filename, "+a") as frames:
        if not first_written_line:
            frames.write("\n")

        frames.write("\t".join(map_str(numbers)))


def read_frequency_relative_errors(filename):

    relative_errors = []

    with open(filename, "r") as frequency:
        for line in frequency.readlines():
            frequency_data_list = line.strip().split("\t")

            last_index = len(frequency_data_list) - 1
            relative_errors.append(float(frequency_data_list[last_index]))

    return relative_errors

def main():
    parameters = Parameters.from_file("input_parameters.json")

    for _ in range(parameters.simulations()):

        calculations = Calculations(parameters)
        plot = Plot()
        state = State.from_file("input_initState.json", parameters)

        for _ in range(parameters.simulation_frames()):

            filename = f"frames{parameters.simulation()}.txt"
            write_numbers(filename, state.positions)

            current_displacements = state.current_displacements()
            current_velocities = state.current_velocities()
            current_accelerations = state.current_accelerations()
            current_time = state.current_time()

            calculations.register_displacements_and_velocities(
                current_displacements,
                current_velocities,
                current_time
            )

            middle = parameters.middle_index()

            plot.register_oscilator_state(
                current_displacements[middle],
                current_velocities[middle],
                current_accelerations[middle],
                current_time
            )

            state.update()

            parameters.next_frame()

        total, kinetic, potential = calculations.calc_E()

        if parameters.analitic_frequency != None:
            omega_approx = calculations.mean_frequency()

            if omega_approx == None:
                print(f"T_avg = 0 for dt = {parameters.dt()}")

            write_numbers("frequencies.txt", [
                parameters.analitic_frequency,
                omega_approx,
                Calculations.relative_error(
                    parameters.analitic_frequency,
                    omega_approx
                )
            ])

        if parameters.oscilator_amount > 100 and parameters.first_open and parameters.last_open:
            wave_velocity_approx = calculations.calc_wave_vel()
            wave_velocity_analitic = calculations.calc_wave_vel_analitic()

            write_numbers("v_wave.txt", [
                wave_velocity_analitic,
                wave_velocity_approx,
                Calculations.relative_error(
                    wave_velocity_analitic,
                    wave_velocity_approx
                )
            ])

        plot.kinematics("kinematics.png")

        plot.register_energy(total, kinetic, potential)

        plot.energy("Energy.png")

        parameters.next_simulation()

    if parameters.analitic_frequency != None:
        relative_errors = read_frequency_relative_errors("frequencies.txt")

        plot.register_relative_errors(relative_errors, parameters.dts)

        plot.relative_errors("freq_vs_dt.png")


if __name__ == "__main__":
    main()