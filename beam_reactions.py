# Dibuja viga de longitud L con apoyos "pinned" o "roller" y calcula las reacciones

import matplotlib.pyplot as plt

# Seccion 1: Viga | Apoyos | Carga ⬇︎

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
            
v = Beam(1497.35)
v.add_support('pinned', 0)
v.add_support('roller', v.L)
v.add_load(v.L/2, 69, 'down')
v.reactions()
            


# Seccion 2: Gráfica ⬇︎

fig, ax = plt.subplots()

# dibujar viga
ax.hlines(y=0, xmin=0, xmax=v.L, color='black', linewidth=3)

# dibujar apoyos
l = v.L/34   # real = 2*l   # longitud apoyo
h = v.L/17   # altura apoyo
    
def draw_sub_support(pos):   # dibujar sub-apoyo (sombra)
    sub_l = l + l*0.35   # longitud sub-apoyo
    sub_h = h + l*0.45   # altura sub-apoyo
    ax.hlines(y=-h, xmin=pos-sub_l, xmax=pos+sub_l, color='black')
    ax.fill((pos-sub_l, pos+sub_l, pos+sub_l, pos-sub_l), (-h, -h, -sub_h, -sub_h), color='#CBCBCB')

def draw_support(support):
    if support.support_type == 'pinned':
        ax.fill((support.pos-l, support.pos+l, support.pos, support.pos-l), (-h, -h, 0, -h), color='#264F92')
        draw_sub_support(support.pos)
    elif support.support_type == 'roller':
        r = v.L/85
        ax.fill((support.pos-l, support.pos+l, support.pos, support.pos-l), (-(h-2*r), -(h-2*r), 0, -(h-2*r)), color='#264F92')
        circle1 = plt.Circle((support.pos-(l-r), -(h-r)), r, color='#264F92')
        circle2 = plt.Circle((support.pos+(l-r), -(h-r)), r, color='#264F92')
        ax.add_artist(circle1)
        ax.add_artist(circle2)
        draw_sub_support(support.pos)
    
for support in v.supports:
    draw_support(support)

# no mostrar ejes
ax.yaxis.set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# plt.tight_layout()
plt.axis('equal')   # 'equal' | 'scaled' | 'tight' | 'auto' | 'image' | 'square'
# plt.grid(linewidth=0.2)
# ax.set_axisbelow(True)   # cuadrícula detrás de la gráfica
plt.show()