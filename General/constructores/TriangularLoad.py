# creador de cargas distribuidas triangulares simples (comienzan o terminan con magnitud 0)
class TriangularLoad:
    def __init__(self, start_pos, end_pos, load, a_d, d="down", node_id=None):
        self.type = "triangular"
        self.start_pos = start_pos  # posición inicial
        self.end_pos = end_pos  # posición final
        self.length = end_pos - start_pos  # longitud
        self.load = load  # magnitud carga
        self.a_d = a_d  # dirección carga ('ascending' o 'descending')
        self.d = d  # dirección carga ('up' o 'down')
        self.node_id = node_id  # id nodo
        # definir posición
        if a_d == "ascending":
            self.pos = start_pos + (2 / 3) * (end_pos - start_pos)
        elif a_d == "descending":
            self.pos = start_pos + (1 / 3) * (end_pos - start_pos)
