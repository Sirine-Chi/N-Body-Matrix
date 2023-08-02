import n_body_lib as nbl

class Simulator:
    def __init__(self, objects):
        self.objects = objects
        self.begin_time = nbl.time.time()
    
    def get_last_coordinates() -> list:
        pass

    def visualise():
        positions = []
        masses = []
        times = []
        return {
			"times": times,
			"positions": positions,
			"masses": masses
		}
    
class Objected_Simulator(Simulator):
    pass

class GPU_Simulator(Simulator):
    pass