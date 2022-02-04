import json
import os


def read_input_parameters():
    with open("input_parameters.json", "r") as parameters:
        unparsed_parameters = parameters.read()
        return json.loads(unparsed_parameters)
    

def read_particle_state():
    with open("input_initState.json", "r") as state:
        unparsed_state = state.read()
        return json.loads(unparsed_state)


def write_positions(particle_positions):

    def map_str(sequence):
        for i in range(len(sequence)):
            sequence[i] = str(sequence[i])

    map_str(particle_positions)

    first_written_line = not os.path.exists("frames.txt")

    with open("frames.txt", "+a") as frames:
        if not first_written_line:
            frames.write("\n")

        frames.write("\t".join(particle_positions))


def main():
    parameters = read_input_parameters()
    state = read_particle_state()

    for _ in parameters["frames_num"]:
        write_positions(state["x_init"])


if __name__ == "__main__":
    main()