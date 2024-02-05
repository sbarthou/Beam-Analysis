# creador de cargas distribuidas
class DistributedLoad:
    def __init__(self, start_pos, end_pos, load, d="down", node_id=None):
        self.type = "distributed"
        self.start_pos = start_pos  # posición inicial
        self.end_pos = end_pos  # posición final
        self.length = end_pos - start_pos  # longitud
        self.pos = (start_pos + end_pos) / 2
        self.load = load  # magnitud carga
        self.d = d  # dirección carga ('up' o 'down')
        self.node_id = node_id  # id nodo
