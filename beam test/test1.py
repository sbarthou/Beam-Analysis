import matplotlib.pyplot as plt

# Seccion 1: Viga | Apoyos | Cargas ⬇︎

# longitud viga
L = 10

# apoyos
class Support:
    def __init__(self, support_type, x):
        self.support_type = support_type   # pinned , roller
        self.reactions = None   # número de reacciones
        self.x = x   # posición apoyo
        
    if support_type == 'pinned':
        self.reactions = 2
    elif support_type == 'roller':
        self.reactions = 1


support_type = None
supports = [[0, 0], [1, L]]   # [[<support_type>, <x_position>]]

# cargas
def point_load(x, P, d):   # x: posición carga , P: magnitud carga , d: dirección carga ('up' o 'down')
    



# Seccion 2: Gráfica ⬇︎

fig, ax = plt.subplots()

# dibujar viga
ax.hlines(y=0, xmin=0, xmax=L, color='black', linewidth=3)

# dibujar apoyos
l = L/34   # longitud apoyo   # real = 2*l
h = L/17   # altura apoyo
    
def draw_sub_support(x):   # dibujar sub-apoyo (sombra) | x: posición apoyo
    sub_l = l + l*0.35   # longitud sub-apoyo
    sub_h = h + l*0.45   # altura sub-apoyo
    ax.hlines(y=-h, xmin=x-sub_l, xmax=x+sub_l, color='black')
    ax.fill((x-sub_l, x+sub_l, x+sub_l, x-sub_l), (-h, -h, -sub_h, -sub_h), color='#CBCBCB')

def draw_support(support_type, x):   # dibujar apoyo | support_type: tipo apoyo , x: posición apoyo
    if support_type == 0:
        ax.fill((x-l, x+l, x, x-l), (-h, -h, 0, -h), color='#264F92')
        draw_sub_support(x)
    elif support_type == 1:
        r = L/85
        ax.fill((x-l, x+l, x, x-l), (-(h-2*r), -(h-2*r), 0, -(h-2*r)), color='#264F92')
        circle1 = plt.Circle((x-(l-r), -(h-r)), r, color='#264F92')
        circle2 = plt.Circle((x+(l-r), -(h-r)), r, color='#264F92')
        ax.add_artist(circle1)
        ax.add_artist(circle2)
        draw_sub_support(x)
    
for support in supports:
    a, b = support   # a: tipo apoyo , b: posición apoyo
    draw_support(a, b)

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