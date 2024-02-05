# creador de cargas distribuidas trapezoidales
class TrapezoidalLoad:
    def __init__(self, start_pos, end_pos, start_load, end_load, d="down", node_id=None):
        self.type = "trapezoidal"
        self.start_pos = start_pos  # posición inicial
        self.end_pos = end_pos  # posición final
        self.length = end_pos - start_pos  # longitud
        self.start_load = start_load  # carga inicial
        self.end_load = end_load  # carga final
        self.d = d  # dirección carga ('up' o 'down')
        self.node_id = node_id  # id nodo

        # definir ascending o descending
        if abs(end_load) > abs(start_load):
            self.a_d = "ascending"
        elif abs(end_load) < abs(start_load):
            self.a_d = "descending"
        
        # definir posiciones para cargas equivalentes
        # distribuida rectangular
        self.rectangle_pos = start_pos + (self.length / 2)
        # distribuida triangular
        if self.a_d == "ascending":
            self.triangle_pos = start_pos + ((2 / 3) * self.length)
        elif self.a_d == "descending":
            self.triangle_pos = start_pos + ((1 / 3) * self.length)