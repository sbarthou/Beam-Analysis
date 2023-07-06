# Caso hipotético: viga simplemente apoyada con una carga puntual en el centro
# Calcula: reacciones | fuerza cortante | momento flector
# Dibuja: viga | apoyos "pinned" o "roller" | carga puntual | reacciones | diagrama fuerza cortante | diagrama momento flector

import numpy as np
import matplotlib.pyplot as plt

class Beam:
    def __init__(self, L):
        self.L = L   # largo viga
        self.support_id = 0   # id apoyo
        self.supports = []   # [Support, support_id]
        self.nodes = []   # [Node]
        
    # creador de apoyos
    class Support:
        def __init__(self, support_type, pos):
            self.support_type = support_type   # pinned , roller
            self.xreaction = None   # reacción en x
            self.yreaction = None   # reacción en y
            self.pos = pos   # posición apoyo
            self.id = int   # id apoyo

    # creador de nodos
    class Node:
        def __init__(self, node_type, pos, support_id):
            self.type = node_type   # tipo de nodo ('support' o 'load')
            self.pos = pos   # posición nodo
            self.id = support_id   # id apoyo (si es apoyo) o None (si es carga)
            self.load = None   # carga en nodo
    
    # agregar apoyos
    def add_support(self, support_type, pos):
        self.support_id += 1   # contador id apoyo
        self.supports.append([self.Support(support_type, pos), self.support_id])
        self.nodes.append(self.Node('support', pos, self.support_id))
    
    # agregar carga puntual
    def add_load(self, pos, P, d):
        self.load_pos = pos   # posición carga
        self.point_load = P   # magnitud carga
        self.load_d = d   # dirección carga ('up' o 'down')
        if d == 'down':
            self.point_load = -P   # signo carga (positivo hacia arriba, negativo hacia abajo)
        self.nodes.append(self.Node('load', pos, None))
    
    # calcular reacciones
    def reactions(self):
        for support_list in self.supports:
            support = support_list[0]
            # Fx
            support.xreaction = 0
            # Fy
            support.yreaction = -round(self.point_load/2, 2)
            
    # almacenar todas las cargas
    def loads(self):
        sorted_supports_id = sorted(self.supports, key=lambda x: x[1])   # ordenar apoyos por id
        suppport_id = 0   # contador id apoyo
        for node in self.nodes:
            if node.type == 'load':
                node.load = self.point_load
            elif node.type == 'support':
                node.load = self.supports[suppport_id][0].yreaction
                suppport_id += 1
        
        self.nodes = sorted(self.nodes, key=lambda x: x.pos)   # ordenar nodos por posición

        
    # artistas de viga
    # dibujar viga
    def draw_beam(self):
        ax.hlines(y=0, xmin=0, xmax=self.L, color='black', linewidth=3)
        
    # dibujar apoyos
    def draw_supports(self):
        l = self.L/34   # real = 2*l   # longitud apoyo
        h = self.L/17   # altura apoyo
        
        # dibujar sub-apoyo (sombra)    
        def sub_support(pos):   
            sub_l = l + l*0.35   # longitud sub-apoyo
            sub_h = h + l*0.45   # altura sub-apoyo
            ax.hlines(y=-h, xmin=pos-sub_l, xmax=pos+sub_l, color='black')
            ax.fill((pos-sub_l, pos+sub_l, pos+sub_l, pos-sub_l), (-h, -h, -sub_h, -sub_h), color='#CBCBCB')
            
        def drawSupports(support_list):
            support = support_list[0]
            if support.support_type == 'pinned':
                ax.fill((support.pos-l, support.pos+l, support.pos, support.pos-l), (-h, -h, 0, -h), color='#264F92')
                sub_support(support.pos)
            elif support.support_type == 'roller':
                r = self.L/85
                ax.fill((support.pos-l, support.pos+l, support.pos, support.pos-l), (-(h-2*r), -(h-2*r), 0, -(h-2*r)), color='#264F92')
                circle1 = plt.Circle((support.pos-(l-r), -(h-r)), r, color='#264F92')
                circle2 = plt.Circle((support.pos+(l-r), -(h-r)), r, color='#264F92')
                ax.add_artist(circle1)
                ax.add_artist(circle2)
                sub_support(support.pos)
                
        for support in self.supports:
            drawSupports(support)
    
    # dibujar carga puntual    
    def draw_load(self):
        arrow_h = self.L/6.8
        arrow_w = self.L/170
        head_w = self.L/(17/0.35)
        text_dy = arrow_h + arrow_h/4
        if self.load_d == 'down':
            ax.arrow(self.load_pos, arrow_h, 0, -arrow_h, width=arrow_w, head_width=head_w, length_includes_head=True, color='black', linewidth=0.5)
            ax.text(self.load_pos, text_dy, f'{abs(self.point_load)} kN', horizontalalignment='center', verticalalignment='center', fontsize=8)
            
    # dibujar reacciones
    def draw_reactions(self):
        for support_list in self.supports:
            support = support_list[0]
            arrow_h = self.L/8.5
            arrow_w = self.L/170
            head_w = self.L/(17/0.35)
            text_dy = arrow_h + arrow_h/4
            if support.yreaction > 0:
                ax.arrow(support.pos, -arrow_h, 0, arrow_h, width=arrow_w, head_width=head_w, length_includes_head=True, facecolor='red', linewidth=0.5)
                ax.text(support.pos, -text_dy, f'{support.yreaction} kN', horizontalalignment='center', verticalalignment='center', fontsize=8)
                
    # dibujar solicitado
    def draw_beam_elements(self, solicitado):   # solicitado = ['beam', 'supports', 'load', 'reactions']
        self.reactions()
        for artist in solicitado:
            if artist == 'beam':
                self.draw_beam()
            elif artist == 'supports':
                self.draw_supports()
            elif artist == 'load':
                self.draw_load()
            elif artist == 'reactions':
                self.draw_reactions()
        if solicitado == ['beam']:
            plt.show()
        else:
            plt.axis('equal')
            plt.show()
    
    # dibujar todo
    def draw_beam_all(self):
        self.reactions()
        self.draw_beam()
        self.draw_supports()
        self.draw_load()
        self.draw_reactions()
        plt.axis('equal')
        plt.show()
        
    # artistas diagramas
    # dibujar diagrama de fuerza cortante
    def draw_shear(self):
        self.reactions()
        self.loads()
        
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
        self.reactions()
        self.loads()
        
        area1 = self.nodes[0].load * self.nodes[1].pos
        area2 = (self.nodes[0].load + self.nodes[1].load) * (self.nodes[2].pos - self.nodes[1].pos)
        
        x = [node.pos for node in self.nodes]
        y = [0, area1, area1+area2]
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
        
        
v = Beam(10)
v.add_support('pinned', 0)
v.add_support('roller', v.L)
v.add_load(v.L/2, 10, 'down')

fig, ax = plt.subplots()

# no mostrar ejes
ax.yaxis.set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
        
v.draw_shear()