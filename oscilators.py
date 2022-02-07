from copy import deepcopy
import json
from math import pi, sqrt
import os
import signal
from matplotlib import pyplot

"""
Reads simulations' parameters from a json file

filename: name of the input file
"""
def params_from_file(filename):
    with open(filename, "r") as params:
        unparsed_params = params.read()
        return json.loads(unparsed_params)

"""
Reads oscilators' initial positions and velocities from a json file

filename: name of the input file
"""
def state_from_file(filename):
    with open(filename, "r") as state:
        unparsed_state = state.read()
        return json.loads(unparsed_state)

"""
Writes a list of numbers to a file.
If the file does not exist, it will be created.
Alternatively, if it does exist, a new line with the numbers
will be appended to it. The numbers will be separated with a tab character

filename: name of the ouput file
numbers: list of numbers to write
"""
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

"""
Reads all the relative frequency errors from a file
and returns them as a list

filename: name of the input file
"""
def read_frequency_relative_errors(filename):

    relative_errors = []

    with open(filename, "r") as frequency:
        for line in frequency.readlines():
            frequency_data_list = line.strip().split("\t")

            last_index = len(frequency_data_list) - 1
            relative_errors.append(float(frequency_data_list[last_index]))

    return relative_errors

"""
Calculates a list of the kinetic energies of the whole system, one for each frame of time

params: dictionary with the simulations' parameters
velocities_list: list of the velocities of all particles, one for each frame of time
one for each frame of time
"""
def calc_kinetic(params, velocities_list):
    kinetic = []

    for velocities in velocities_list:

        kinetic_t = 0

        for i in range(params['osc_num']):
            kinetic_t += velocities[i] ** 2

        kinetic_t *= params['mass'] / 2

        kinetic.append(kinetic_t)
    
    return kinetic

"""
Calculates a list of the potential energies of the whole system, one for each frame of time

params: dictionary with the simulations' parameters
displacements_list: list of the displacements from the equilibrium point of all particles,
"""
def calc_potential(params, displacements_list):
    potential = []

    for displacements in displacements_list:

        potential_t = 0

        for i in range(params['osc_num'] - 1):
            potential_t += (displacements[i + 1] - displacements[i]) ** 2

        potential_t *= params['k'] / 2

        potential.append(potential_t)
    
    return potential

"""
Calculates a list of the mechanic, kinetic and potential energies, one for each frame of time,
and returns them as a tuple

params: dictionary with the simulations' parameters
displacements_list: list of the displacements from the equilibrium point of all particles,
velocities_list: list of the velocities of all particles, one for each frame of time
one for each frame of time
"""
def calc_E(params, displacements_list, velocities_list):
    kinetic = calc_kinetic(params, velocities_list)
    potential = calc_potential(params, displacements_list)

    total = []
    for k, p in zip(kinetic, potential):
        total.append(k + p)

    return (total, kinetic, potential)

"""
Calculates the mean of the frequencies

params: dictionary with the simulations' parameters
displacements_list: list of the displacements from the equilibrium point of all particles,
one for each frame of time
times: list of each frame of time
"""
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

"""
Calculates the velocity of travel of the wave in the simulation
using an approximation

params: dictionary with the simulations' parameters
velocities_list: list of the velocities of all particles, one for each frame of time
times: list of each frame of time
"""
def calc_wave_vel(params, velocities_list, times):
    last_oscilator_velocities = []

    for velocities in velocities_list:
        last_oscilator_velocity = velocities[len(velocities) - 1]
        last_oscilator_velocities.append(last_oscilator_velocity)

    time_of_movement = 0
    for t, v in zip(times, last_oscilator_velocities):
        time_of_movement = t
        if v > 0:
            break

    spring_amount = params['osc_num'] - 1
    length_of_rest = params['l_rest'] * spring_amount

    return length_of_rest / time_of_movement

"""
Calculates the velocity of travel of the wave in the simulation
using the analitic formula

params: dictionary with the simulations' parameters
"""
def calc_wave_vel_analitic(params):
    return sqrt(params['k'] / params['mass']) * params['l_rest']

"""
Calculates the relative error of a real and meassured quantity

real: real quantity of a value
approx: meassured quantity of that same value
"""
def relative_error(real, approx):
    return abs(real - approx) / real

"""
Plots the displacements from the equilibrium point, velocities, and accelerations
of a single particle in the system as a function of time, for a single simulation

filename: name of the output file
displacements: list of oscilator displacement for each frame of time
velocities: list of oscilator velocity for each frame of time
accelerations: list of oscilator acceleration for each frame of time
times: list of each frame of time
"""
def plot_kinematics(filename, displacements, velocities, accelerations, times):
    fig, axes = pyplot.subplots(1, 3)

    axes[0].plot(times, displacements)
    axes[1].plot(times, velocities)
    axes[2].plot(times, accelerations)

    pyplot.savefig(filename)
    pyplot.close(fig)

"""
Plots the total, kinetic, and potenial energy as a function of time
for a single simulation

filename: name of the output file
total: list of mechanic energy of the whole system for each frame of time
kinetic: list of kinetic energy of the whole system for each frame of time
potential: list of potential energy of the whole system for each frame of time
times: list of each frame of time
"""
def plot_energy(filename, total, kinetic, potential, times):
    fig, axes = pyplot.subplots(1, 3)

    axes[0].plot(times, total)
    axes[1].plot(times, kinetic)
    axes[2].plot(times, potential)

    pyplot.savefig(filename)
    pyplot.close(fig)

"""
Plots the relative errors of the various angular frequencies
calculated across all the simulations, as a function of the time interval
used in each simulation

filename: name of the output file
errors: list of all relative errors
time_intervals: corresponding list of the time intervals
used for each frequency approximation
"""
def plot_relative_errors(filename, errors, time_intervals):
    fig, axis = pyplot.subplots(1, 1)

    axis.plot(time_intervals, errors)

    pyplot.savefig(filename)
    pyplot.close(fig)

"""
Calculates the force applied to a single oscilator
due to its left spring

params: dictionary with the simulations' parameters
state: dictionary with the current state of all oscilators
i: index of the oscilator to be used
"""
def left_force(params, state, i):
    if i == 0:
        return 0

    if i == params['osc_num'] - 1 and not params['last_is_open']:
        return 0

    return -params['k'] * (state['displacements'][i] - state['displacements'][i - 1])

"""
Calculates the force applied to a single oscilator
due to its right spring

params: dictionary with the simulations' parameters
state: dictionary with the current state of all oscilators
i: index of the oscilator to be used
"""
def right_force(params, state, i):
    if i == params['osc_num'] - 1:
        return 0

    if i == 0 and not params['first_is_open']:
        return 0

    return -params['k'] * (state['displacements'][i] - state['displacements'][i + 1])

"""
Updates the oscilators' state (positions, velocities, accelerations, etc)
using the Leapfrog Method in one small time interval, specified in the parameters.

params: dictionary with the simulations' parameters
state: dictionary with the current state of all oscilators
"""
def update(params, state):
    dt = params['dt'][params['simulation'] - 1]

    for i in range(params['osc_num']):
        net_force = left_force(params, state, i) + right_force(params, state, i)

        state['accelerations'][i] = net_force / params['mass']

        if params['frame'] == 1:
            state['mid_velocities'][i] = state['v'][i] + state['accelerations'][i] * dt / 2
        else:
            state['mid_velocities'][i] += + state['accelerations'][i] * dt

        state['v'][i] = state['mid_velocities'][i] - state['accelerations'][i] * dt / 2

        state['x'][i] += state['mid_velocities'][i] * dt

        state['displacements'][i] = state['x'][i] - i * params['l_rest']

        state['elapsed_time'] += dt

"""
Entry point of the program

Reads information from files and runs all the simulations,
each with its own amount of frames and time interval,
then writes the results to files and images
"""
if __name__ == "__main__":
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

        state = state_from_file("input_initState.json")
        state['displacements'] = []
        state['mid_velocities'] = []
        state['accelerations'] = []
        state['elapsed_time'] = 0

        for _ in range(params['osc_num']):
            state['displacements'].append(0)
            state['mid_velocities'].append(0)
            state['accelerations'].append(0)

        for i in range(params['osc_num']):
            state['displacements'][i] = state['x'][i] - i * params['l_rest']

        for _ in range(params['frames_num'][params['simulation'] - 1]):

            filename = f"frames{params['simulation']}.txt"
            write_numbers(filename, state['x'])

            current_displacements = deepcopy(state['displacements'])
            current_velocities = deepcopy(state['v'])
            current_accelerations = deepcopy(state['accelerations'])

            displacements_list.append(current_displacements)
            velocities_list.append(current_velocities)
            times.append(state['elapsed_time'])

            middle = int(params['osc_num'] / 2)

            middle_displacements.append(current_displacements[middle])
            middle_velocities.append(current_velocities[middle])
            middle_accelerations.append(current_accelerations[middle])

            update(params, state)

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