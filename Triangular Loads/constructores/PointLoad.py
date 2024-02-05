# creador de cargas puntuales
class PointLoad:
    def __init__(self, pos, load, d="down", node_id=None):
        self.type = "point"
        self.pos = pos  # posición carga
        self.load = load  # magnitud carga
        self.d = d  # dirección carga ('up' o 'down')
        self.node_id = node_id  # id nodo
