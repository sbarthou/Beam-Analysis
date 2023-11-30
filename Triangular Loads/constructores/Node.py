# creador de nodos
class Node:
    def __init__(self, node_type, pos, node_id, objeto):
        self.type = node_type  # tipo de nodo ('support' , 'point_load' , 'distributed_load_L' , 'distributed_load_R', 'simple_triangular_load_L', 'simple_triangular_load_R', 'support_load')
        self.pos = pos  # posición nodo
        self.load = None  # carga en nodo
        self.load_num = None  # número de cargas en el nodo
        self.id = node_id  # id nodo
        self.objeto = objeto