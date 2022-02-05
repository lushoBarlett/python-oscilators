import json


class Parameters:
    def from_file(filename):
        with open(filename, "r") as parameters:
            unparsed_parameters = parameters.read()
            parsed_parameters = json.loads(unparsed_parameters)
            return Parameters(parsed_parameters)


    def __init__(self, params):
        self.simulations = []
        for (frames, dt) in zip(params["frames_num"], params["dt"]):
            self.simulations.append((frames, dt))

        self.length_rest = params["l_rest"]
        self.spring_constant = params["k"]
        self.analitic_frequency = params["omega"]

        self.oscilator_amount = params["osc_num"]

        self.first_open = params["first_is_open"]
        self.last_open = params["last_is_open"]
