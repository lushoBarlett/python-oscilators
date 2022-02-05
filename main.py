import os

from parameters import Parameters
from state import State


def write_positions(filename, particle_positions):

    def map_str(sequence):
        result = []
        for element in sequence:
            result.append(str(element))
        return result

    first_written_line = not os.path.exists(filename)

    with open(filename, "+a") as frames:
        if not first_written_line:
            frames.write("\n")

        frames.write("\t".join(map_str(particle_positions)))


def main():
    parameters = Parameters.from_file("input_parameters.json")

    for _ in range(parameters.simulations()):

        state = State.from_file("input_initState.json", parameters)

        for _ in range(parameters.simulation_frames()):

            filename = f"frames{parameters.simulation()}.txt"
            write_positions(filename, state.positions)

            state.update()

            parameters.next_frame()

        parameters.next_simulation()


if __name__ == "__main__":
    main()