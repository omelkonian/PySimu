class State(object):
    """State of the simulation"""
    def __init__(self, number_of_trams, number_of_stops):
        self.end_simulation = False
        self.timetable_generator = self.gen_timetable()
        self.timetable = []
        self.toggle_timetable()
        self.tram_capacity = [0] * number_of_trams
        self.stop_capacity = [0] * number_of_stops
        self.arrivals = [[]] * number_of_stops

    @staticmethod
    def gen_timetable():
        def create_timetable(freq):
            return [(freq * i, False) for i in range(int(60 / freq))]
        while True:
            yield create_timetable(15)
            yield create_timetable(4)

    def toggle_timetable(self):
        self.timetable = next(self.timetable_generator)

    def __str__(self):
        return """
        ============ STATE ============
        Timetable: {0.timetable}
        TramCapacity: {0.tram_capacity}
        StopCapacity: {0.stop_capacity}
        Arrivals: {0.arrivals}
        ===============================
        """.format(self)
