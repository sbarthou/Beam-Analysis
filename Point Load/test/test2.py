# Caso hipotético: viga simplemente apoyada con una carga puntual en el centro
# Calcula: reacciones

import matplotlib.pyplot as plt

# creador de viga
class Beam:
    def __init__(self, L):
        self.L = L
        self.supports = []
    
    # creador de apoyos    
    class Support:
        def __init__(self, support_type, pos):
            self.support_type = support_type   # pinned , roller
            self.xreaction = None   # reacción en x
            self.yreaction = None   # reacción en y
            self.pos = pos   # posición apoyo
    
    # agregar apoyos 
    def add_support(self, support_type, pos):
        self.supports.append(self.Support(support_type, pos))
    
    # agregar carga puntual
    def add_load(self, pos, P, d):
        self.load_pos = pos   # posición carga
        self.load = P   # magnitud carga
        self.load_d = d   # dirección carga ('up' o 'down')
        
        if d == 'down':
            self.load = -P
    
    # calcular reacciones
    def reactions(self):
        for support in self.supports:
            # Fx
            support.xreaction = 0
            # Fy
            support.yreaction = -self.load/2
            
            
v = Beam(10)
v.add_support('pinned', 0)
v.add_support('roller', v.L)
v.add_load(v.L/2, 69, 'down')
v.reactions()

for support in v.supports:
    print(support.xreaction, support.yreaction)