from copy import deepcopy
import json
from math import pi, sqrt
import os
import signal

from matplotlib import pyplot

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

def calc_kinetic(params, velocities_list):
    kinetic = []

    for velocities in velocities_list:

        kinetic_t = 0

        for i in range(params['osc_num']):
            kinetic_t += velocities[i] ** 2

        kinetic_t *= params['mass'] / 2

        kinetic.append(kinetic_t)
    
    return kinetic

def calc_potential(params, displacements_list):
    potential = []

    for displacements in displacements_list:

        potential_t = 0

        for i in range(params['osc_num'] - 1):
            potential_t += (displacements[i + 1] - displacements[i]) ** 2

        potential_t *= params['k'] / 2

        potential.append(potential_t)
    
    return potential

def calc_E(params, displacements_list, velocities):
    kinetic = calc_kinetic(params, velocities)
    potential = calc_potential(params, displacements_list)

    total = []
    for k, p in zip(kinetic, potential):
        total.append(k + p)

    return (total, kinetic, potential)

def mean_frequency(params, displacements_list, times):
    middle_oscilator_displacements = []

    for displacements in displacements_list:
        middle = int(params['osc_num'] / 2)
        middle_oscilator_displacements.append(displacements[middle])

    indices, _ = signal.find_peaks(middle_oscilator_displacements)

    period_approximates = []

    for i in range(len(indices) - 1):
        tmax1 = times[indices[i]]
        tmax2 = times[indices[i + 1]]
        period_approximates.append(abs(tmax1 - tmax2))

    mean_period = 0

    for p in period_approximates:
        mean_period += p

    mean_period /= len(period_approximates)

    if mean_period == 0:
        return None

    return 2 * pi / mean_period

def calc_wave_vel(params, velocities_list, times):
    last_oscilator_velocities = []

    for velocities in velocities_list:
        last_oscilator_velocity = velocities[len(velocities) - 1]
        last_oscilator_velocities.append(last_oscilator_velocity)

    time_of_movement = 0
    for t, v in zip(times, velocities):
        time_of_movement = t
        if v > 0:
            break

    spring_amount = params['osc_num'] - 1
    length_of_rest = params['l_rest'] * spring_amount

    return length_of_rest / time_of_movement

def calc_wave_vel_analitic(params):
    return sqrt(params['k'] / params['mass']) * params['l_rest']

def relative_error(real, approx):
    return abs(real - approx) / real

def plot_kinematics(filename, displacements, velocities, accelerations, times):
    fig, axes = pyplot.subplots(1, 3)

    axes[0].plot(times, displacements)
    axes[1].plot(times, velocities)
    axes[2].plot(times, accelerations)

    pyplot.savefig(filename)
    pyplot.close(fig)

def plot_energy(filename, total, kinetic, potential, times):
    fig, axes = pyplot.subplots(1, 3)

    axes[0].plot(times, total)
    axes[1].plot(times, kinetic)
    axes[2].plot(times, potential)

    pyplot.savefig(filename)
    pyplot.close(fig)

def plot_relative_errors(filename, errors, time_intervals):
    fig, axis = pyplot.subplots(1, 1)

    axis.plot(time_intervals, errors)

    pyplot.savefig(filename)
    pyplot.close(fig)

def main():
    params = params_from_file("input_parameters.json")
    params['simulation'] = 1
    params['frame'] = 1

    for _ in params['frames_num']:

        displacements_list = []
        velocities_list = []
        times = []

        middle_displacements = []
        middle_velocities = []
        middle_accelerations = []

        state = state_from_file("input_initState.json", params)

        for _ in range(params['frames_num'][params['simulation'] - 1]):

            filename = f"frames{params['simulation']}.txt"
            write_numbers(filename, state.positions)

            current_displacements = deepcopy(state.displacements)
            current_velocities = deepcopy(state.velocities)
            current_accelerations = deepcopy(state.accelerations)

            displacements_list.append(current_displacements)
            velocities_list.append(current_velocities)
            times.append(state.elapsed_time)

            middle = int(params['osc_num'] / 2)

            middle_displacements.append(current_displacements[middle])
            middle_velocities.append(current_velocities[middle])
            middle_accelerations.append(current_accelerations[middle])

            state.update()

            params['frame'] += 1

        total, kinetic, potential = calc_E(params, displacements_list, velocities_list)

        if params['omega'] != None:
            omega_approx = mean_frequency(params, displacements_list, times)

            if omega_approx == None:
                print(f"T_avg = 0 for dt = {params['dt'][params['simulation'] - 1]}")

            write_numbers("frequencies.txt", [
                params['omega'],
                omega_approx,
                relative_error(params['omega'], omega_approx)
            ])

        if params['osc_num'] > 100 and params['first_is_open'] and params['last_is_open']:
            wave_velocity_approx = calc_wave_vel(params, velocities_list, times)
            wave_velocity_analitic = calc_wave_vel_analitic(params)

            write_numbers("v_wave.txt", [
                wave_velocity_analitic,
                wave_velocity_approx,
                relative_error(wave_velocity_analitic, wave_velocity_approx)
            ])

        plot_kinematics(
            "kinematics.png",
            middle_displacements,
            middle_velocities,
            middle_accelerations,
            times
        )

        plot_energy(
            "Energy.png",
            total,
            kinetic,
            potential,
            times
        )

        params['simulation'] += 1
        params['frame'] = 1

    if params['omega'] != None:
        errors = read_frequency_relative_errors("frequencies.txt")

        plot_relative_errors(
            "freq_vs_dt.png",
            errors,
            params['dt']
        )


if __name__ == "__main__":
    main()