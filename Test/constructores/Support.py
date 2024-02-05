# creador de apoyos
class Support:
    def __init__(self, support_type, pos, node_id):
        self.type = support_type  # pinned , roller
        self.pos = pos  # posición apoyo
        self.yreaction = None  # reacción en y
        self.node_id = node_id  # id nodo
