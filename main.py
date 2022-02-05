import os

from parameters import Parameters
from state import State


def write_positions(filename, particle_positions):

    def map_str(sequence):
        for i in range(len(sequence)):
            sequence[i] = str(sequence[i])

    map_str(particle_positions)

    first_written_line = not os.path.exists(filename)

    with open(filename, "+a") as frames:
        if not first_written_line:
            frames.write("\n")

        frames.write("\t".join(particle_positions))


def main():
    parameters = Parameters.from_file("input_parameters.json")
    state = State.from_file("input_initState.json")

    for simulation, (frames, dt) in enumerate(parameters.simulations, 1):
        for _ in range(frames):
            write_positions(f"frames{simulation}.txt", state.positions)


if __name__ == "__main__":
    main()