# creador de apoyos
class Support:
    def __init__(self, support_type: str, pos, node_id: int):
        self.type = support_type  # pinned , roller , fixed
        self.pos = pos  # posición apoyo
        self.yreaction = None  # reacción en y
        self.node_id = node_id  # id nodo
