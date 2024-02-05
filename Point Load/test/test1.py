# Caso hipotético: viga simplemente apoyada con una carga puntual en el centro
# Calcula: reacciones

import matplotlib.pyplot as plt

# Seccion 1: Viga | Apoyos | Cargas ⬇︎

# longitud viga
L = 10

# apoyos
class Support:
    def __init__(self, support_type, pos):
        self.support_type = support_type   # pinned , roller
        self.xreaction = None   # reacción en x
        self.yreaction = None   # reacción en y
        self.pos = pos   # posición apoyo
        
# carga puntual
class PointLoad:
    def __init__(self, pos, P, d):
        self.pos = pos   # posición carga
        self.P = P   # magnitud carga
        self.d = d   # dirección carga ('up' o 'down')
        
        if d == 'down':
            self.P = -P

# reacciones
def reactions(supports, load):
    for support in supports:
        # Fx
        support.xreaction = 0
        
        # Fy
        support.yreaction = -load.P/2
        
        
supports = [Support('pinned', 0), Support('roller', L)]
load = PointLoad(L/2, 69, 'down')
reactions(supports, load)

print(f'Reacciones soporte 1: Rx = {supports[0].xreaction} , Ry = {supports[0].yreaction}')
print(f'Reacciones soporte 2: Rx = {supports[1].xreaction} , Ry = {supports[1].yreaction}')