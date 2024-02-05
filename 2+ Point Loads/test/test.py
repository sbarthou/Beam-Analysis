# Caso hipotético: viga simplemente apoyada con dos cargas puntuales
# Calcula: reacciones | fuerza cortante | momento flector
# Dibuja: viga | apoyos "pinned" o "roller" | carga puntual | reacciones | diagrama fuerza cortante | diagrama momento flector

import numpy as np
import matplotlib.pyplot as plt

# creador de viga
class Beam:
    def __init__(self, L):
        self.L = L   # largo viga
        # self.node_id_count = 0   # contador id nodo (comienza en 0)
        self.nodes = []   # [Node]
        self.support_id_count = 0   # contador id apoyo (comienza en 0)
        self.supports = []   # [Support]
        self.load_id_count = 0   # contador id carga (comienza en 0)
        self.loads = []   # [Load]
        
    # creador de nodos
    class Node:
        def __init__(self, node_type, pos, type_node_id):
            self.type = node_type   # tipo de nodo ('support' o 'load')
            self.pos = pos   # posición nodo
            self.load = None   # carga en nodo
            self.id = type_node_id   # support id (si es apoyo) o load id (si es carga)
        
    # creador de apoyos
    class Support:
        def __init__(self, support_type, pos, support_id_count):
            self.support_type = support_type   # pinned , roller
            self.pos = pos   # posición apoyo
            self.yreaction = None   # reacción en y
            self.id = support_id_count   # id apoyo
            
    # creador de cargas
    class Load:
        def __init__(self, pos, P, d, load_id_count):
            self.pos = pos   # posición carga
            self.P = P   # magnitud carga
            self.d = d   # dirección carga ('up' o 'down')
            self.id = load_id_count   # id carga
    
    # agregar apoyos
    def add_support(self, support_type, pos):
        self.supports.append(self.Support(support_type, pos, self.support_id_count))
        self.nodes.append(self.Node('support', pos, self.support_id_count))
        self.support_id_count += 1   # contador id apoyo
        
    # agregar carga puntual
    def add_load(self, pos, P, d):
        if d == 'down':
            P = -P   # signo carga (positivo hacia arriba, negativo hacia abajo)
        self.loads.append(self.Load(pos, P, d, self.load_id_count))
        self.nodes.append(self.Node('load', pos, self.load_id_count))
        self.load_id_count += 1   # contador id carga
    
    # calcular reacciones
    def reactions(self):
        Ay = 0   # reacción apoyo A en eje y
        By = 0   # reacción apoyo B en eje y
        # Fy = 0
        sum_loads = sum([load.P for load in self.loads])   # suma de todas las cargas, las cargas quedan igualadas a este valor (Ay + By = sum_loads)
        # M = 0 (respecto al primer apoyo (A))
        self.supports[1].yreaction = -(self.loads[0].P * self.loads[0].pos + self.loads[1].P * self.loads[1].pos)/self.L   # reacción segundo soporte (B)
        self.supports[0].yreaction = -sum_loads - self.supports[1].yreaction   # reacción primer soporte (A)
            
        self.supports = sorted(self.supports, key=lambda x: x.pos)   # ordenar apoyos por posición
        
    # almacenar todas las cargas
    def forces(self):
        self.reactions()
        support_id = 0   # contador interno support_id
        load_id = 0   # contador interno load_id
        for node in self.nodes:
            if node.type == 'support':
                node.load = self.supports[support_id].yreaction
                support_id += 1
            elif node.type == 'load':
                node.load = self.loads[load_id].P
                load_id += 1
    
        self.nodes = sorted(self.nodes, key=lambda x: x.pos)   # ordenar nodos por posición
    
    
    # artistas de viga    
    # dibujar viga
    def draw_beam(self, AX=0):
        if AX == 0:
            ax.hlines(y=0, xmin=0, xmax=self.L, color='black', linewidth=3)
        else:
            AX.hlines(y=0, xmin=0, xmax=self.L, color='black', linewidth=3)
            # no mostrar ejes
            AX.xaxis.set_visible(False)
            AX.yaxis.set_visible(False)
        
    # dibujar apoyos
    def draw_supports(self, AX=0):
        l = self.L/34   # real = 2*l   # longitud apoyo
        h = self.L/17   # altura apoyo
        
        # dibujar sub-apoyo (sombra)    
        def sub_support(pos):   
            sub_l = l + l*0.35   # longitud sub-apoyo
            sub_h = h + l*0.45   # altura sub-apoyo
            if AX == 0:
                ax.hlines(y=-h, xmin=pos-sub_l, xmax=pos+sub_l, color='black')
                ax.fill((pos-sub_l, pos+sub_l, pos+sub_l, pos-sub_l), (-h, -h, -sub_h, -sub_h), color='#CBCBCB')
            else:
                AX.hlines(y=-h, xmin=pos-sub_l, xmax=pos+sub_l, color='black')
                AX.fill((pos-sub_l, pos+sub_l, pos+sub_l, pos-sub_l), (-h, -h, -sub_h, -sub_h), color='#CBCBCB')
            
        def drawSupports(support):
            if support.support_type == 'pinned':
                if AX == 0:
                    ax.fill((support.pos-l, support.pos+l, support.pos, support.pos-l), (-h, -h, 0, -h), color='#264F92')
                else:
                    AX.fill((support.pos-l, support.pos+l, support.pos, support.pos-l), (-h, -h, 0, -h), color='#264F92')
                sub_support(support.pos)
            elif support.support_type == 'roller':
                r = self.L/85
                circle1 = plt.Circle((support.pos-(l-r), -(h-r)), r, color='#264F92')
                circle2 = plt.Circle((support.pos+(l-r), -(h-r)), r, color='#264F92')
                if AX == 0:
                    ax.fill((support.pos-l, support.pos+l, support.pos, support.pos-l), (-(h-2*r), -(h-2*r), 0, -(h-2*r)), color='#264F92')
                    ax.add_artist(circle1)
                    ax.add_artist(circle2)
                else:
                    AX.fill((support.pos-l, support.pos+l, support.pos, support.pos-l), (-(h-2*r), -(h-2*r), 0, -(h-2*r)), color='#264F92')
                    AX.add_artist(circle1)
                    AX.add_artist(circle2)
                sub_support(support.pos)
                
        for support in self.supports:
            drawSupports(support)
    
    # dibujar cargas    
    def draw_loads(self):
        for load in self.loads:
            arrow_h = self.L/6.8
            arrow_w = self.L/170
            head_w = self.L/(17/0.35)
            text_dy = arrow_h + arrow_h/4
            if load.d == 'down':
                ax.arrow(load.pos, arrow_h, 0, -arrow_h, width=arrow_w, head_width=head_w, length_includes_head=True, color='black', linewidth=0.5)
                ax.text(load.pos, text_dy, f'{abs(load.P)} kN', horizontalalignment='center', verticalalignment='center', fontsize=8)
                
    # dibujar reacciones
    def draw_reactions(self):
        for support in self.supports:
            arrow_h = self.L/8.5
            arrow_w = self.L/170
            head_w = self.L/(17/0.35)
            text_dy = arrow_h + arrow_h/4
            if support.yreaction > 0:
                ax.arrow(support.pos, -arrow_h, 0, arrow_h, width=arrow_w, head_width=head_w, length_includes_head=True, facecolor='red', linewidth=0.5)
                ax.text(support.pos, -text_dy, f'{round(support.yreaction, 2)} kN', horizontalalignment='center', verticalalignment='center', fontsize=8)   # reacción redondeada a 2 decimales
    
    # dibujar solicitado
    def draw_beam_elements(self, solicitado):   # solicitado = ['beam', 'supports', 'loads', 'reactions']
        self.reactions()
        for artist in solicitado:
            if artist == 'beam':
                self.draw_beam()
            elif artist == 'supports':
                self.draw_supports()
            elif artist == 'loads':
                self.draw_loads()
            elif artist == 'reactions':
                self.draw_reactions()
        if solicitado == ['beam']:
            plt.show()
        else:
            plt.axis('equal')
            plt.show()
            
    # dibujar todos los elementos de la viga
    def draw_beam_all(self, ax=None):
        self.reactions()
        if ax is None:
            fig, ax = plt.subplots()
        self.draw_beam()
        self.draw_supports()
        self.draw_loads()
        self.draw_reactions()
        plt.axis('equal')
        plt.show()
        
        
    # artistas diagramas
    # dibujar diagrama de fuerza cortante
    def draw_shear(self):
        self.forces()
        
        x = []
        y = []
        
        for i in range(len(self.nodes)):
            x.append(self.nodes[i].pos)
            x.append(self.nodes[i].pos)
            if i == 0:
                y.append(0)
                y.append(y[-1] + self.nodes[i].load)
            else:
                y.append(y[-1])
                y.append(y[-1] + self.nodes[i].load)
                
        ax.plot(x, y)
        ax.fill_between(x, y, color='#328DCB', alpha=0.5)
        
        y_max = max(abs(np.asarray(y)))
        ax.set_ylim(-(y_max * 2), (y_max * 2))
        # ax.set_aspect(0.3)
        
        ax.yaxis.set_visible(True)
        ax.spines['left'].set_visible(True)
        ax.grid(linewidth=0.2)   # cuadrícula
        ax.minorticks_on()   # sub valores ejes
        ax.grid(linewidth=0.1, which='minor', linestyle=':')   # sub cuadrícula
        ax.set_axisbelow(True)   # cuadrícula detrás de la gráfica
        ax.set_title('Diagrama de fuerza cortante')
        
        self.draw_beam_elements(['beam'])
        
    # dibujar diagrama de momento flector (método de areas)
    def draw_moment(self):
        self.forces()
        
        area1 = self.nodes[0].load * self.nodes[1].pos
        area2 = (self.nodes[0].load + self.nodes[1].load) * (self.nodes[2].pos - self.nodes[1].pos)
        area3 = (self.nodes[0].load + self.nodes[1].load + self.nodes[2].load) * (self.nodes[3].pos - self.nodes[2].pos)
        
        x = [node.pos for node in self.nodes]
        y = [0, area1, area1+area2, area1+area2+area3]
        
        ax.plot(x, y)
        ax.fill_between(x, y, color='#328DCB', alpha=0.5)

        y_max = max(abs(np.asarray(y)))
        ax.set_ylim(-(y_max * 2), (y_max * 2))
        
        ax.yaxis.set_visible(True)
        ax.spines['left'].set_visible(True)
        ax.grid(linewidth=0.2)   # cuadrícula
        ax.minorticks_on()   # sub valores ejes
        ax.grid(linewidth=0.1, which='minor', linestyle=':')   # sub cuadrícula
        ax.set_axisbelow(True)   # cuadrícula detrás de la gráfica
        ax.set_title('Diagrama de momento flector')
        ax.invert_yaxis()
        self.draw_beam_elements(['beam'])
        
        
    # dibujar todo
    def draw_all(self):
        plt.close()
        fig, ax = plt.subplots(2, 2)
        
        
        
        plt.show()
        
        
        
v = Beam(10)
v.add_support('pinned', 0)
v.add_support('pinned', v.L)
v.add_load(4, 17, 'down')
v.add_load(7, 11, 'down')

fig, ax = plt.subplots()

# no mostrar ejes
ax.yaxis.set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
        
# v.draw_beam_elements(['beam'])
v.draw_beam_elements(['beam', 'supports'])