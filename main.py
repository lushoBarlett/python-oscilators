from cmath import sqrt
import os
from calculations import Calculations

from parameters import Parameters
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


def main():
    parameters = Parameters.from_file("input_parameters.json")

    for _ in range(parameters.simulations()):

        calculations = Calculations(parameters)
        state = State.from_file("input_initState.json", parameters)

        for _ in range(parameters.simulation_frames()):

            filename = f"frames{parameters.simulation()}.txt"
            write_numbers(filename, state.positions)

            calculations.register_displacements_and_velocities(
                state.current_displacements(),
                state.current_velocities(),
                state.current_time()
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

        parameters.next_simulation()


if __name__ == "__main__":
    main()