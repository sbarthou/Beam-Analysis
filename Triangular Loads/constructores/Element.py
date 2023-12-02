# creador de elementos
class Element:
    def __init__(self, l_node, r_node, subx=0):
        self.l_node = l_node  # nodo en extremo izquierdo
        self.r_node = r_node  # nodo en extremo derecho
        self.length = r_node.pos - l_node.pos  # largo del elemento
        self.subx = subx  # número que se le restará a x al calcular el momento
