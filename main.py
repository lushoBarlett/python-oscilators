import json
import os

from calculations import Calculations
from plot import Plot
from state import State

def params_from_file(filename):
    with open(filename, "r") as params:
        unparsed_params = params.read()
        return json.loads(unparsed_params)

def state_from_file(filename, params):
    with open(filename, "r") as state:
        unparsed_state = state.read()
        parsed_state = json.loads(unparsed_state)
        return State(parsed_state, params)

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
    params = params_from_file("input_params.json")
    params['simulation'] = 1
    params['frame'] = 1

    for _ in params['frames_num']:

        calculations = Calculations(params)
        plot = Plot()
        state = state_from_file("input_initState.json", params)

        for _ in range(params['frames_num'][params['simulation'] - 1]):

            filename = f"frames{params['simulation']}.txt"
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

            middle = int(params['osc_num'] / 2)

            plot.register_oscilator_state(
                current_displacements[middle],
                current_velocities[middle],
                current_accelerations[middle],
                current_time
            )

            state.update()

            params['frame'] += 1

        total, kinetic, potential = calculations.calc_E()

        if params['omega'] != None:
            omega_approx = calculations.mean_frequency()

            if omega_approx == None:
                print(f"T_avg = 0 for dt = {params['dt'][params['simulation'] - 1]}")

            write_numbers("frequencies.txt", [
                params['omega'],
                omega_approx,
                Calculations.relative_error(
                    params['omega'],
                    omega_approx
                )
            ])

        if params['osc_num'] > 100 and params['first_is_open'] and params['last_is_open']:
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

        params['simulation'] += 1
        params['frame'] = 1

    if params['omega'] != None:
        relative_errors = read_frequency_relative_errors("frequencies.txt")

        plot.register_relative_errors(relative_errors, params['dt'])

        plot.relative_errors("freq_vs_dt.png")


if __name__ == "__main__":
    main()