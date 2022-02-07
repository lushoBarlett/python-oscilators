import json


class Parameters:

    def from_file(filename):
        with open(filename, "r") as parameters:
            unparsed_parameters = parameters.read()
            parsed_parameters = json.loads(unparsed_parameters)
            return Parameters(parsed_parameters)

    def __init__(self, params):
        self.current_simulation = 1
        self.current_frame = 1
        self.frame_amounts = []
        self.dts = []

        for (frame_amounts, dt) in zip(params["frames_num"], params["dt"]):
            self.frame_amounts.append(frame_amounts)
            self.dts.append(dt)

        self.rest_length = params["l_rest"]
        self.spring_constant = params["k"]
        self.analitic_frequency = params["omega"]

        self.oscilator_amount = params["osc_num"]
        self.oscilator_mass = params["mass"]

        self.first_open = params["first_is_open"]
        self.last_open = params["last_is_open"]

    def simulations(self):
        return len(self.frame_amounts)

    def simulation_frames(self):
        return self.frame_amounts[self.current_simulation - 1]

    def simulation(self):
        return self.current_simulation

    def frame(self):
        return self.current_frame

    def dt(self):
        return self.dts[self.current_simulation - 1]

    def next_simulation(self):
        self.current_simulation += 1
        self.current_frame = 1

    def next_frame(self):
        self.current_frame += 1

    def middle_index(self):
        return int(self.oscilator_amount / 2)