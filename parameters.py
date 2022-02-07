class Parameters:

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