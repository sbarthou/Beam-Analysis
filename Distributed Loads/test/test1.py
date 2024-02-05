# Caso hipotético: viga simplemente apoyada con cargas puntuales y/o distribuídas uniformes
# Calcula: reacciones
# Dibuja: viga | apoyos "pinned" o "roller" | carga puntual | carga distribuída uniforme | reacciones
import numpy as np
import matplotlib.pyplot as plt

# creador de viga
class Beam:
    def __init__(self, L):
        self.L = L   # largo viga
        self.nodes = []   # [Node]
        self.supports = []   # [Support]
        self.loads = []   # [Load, type]
        self.eq_loads = []   # [Load]
        
    # creador de nodos
    class Node:
        def __init__(self, node_type, pos):
            self.type = node_type   # tipo de nodo ('support' o 'load')
            self.pos = pos   # posición nodo
            self.load = None   # carga en nodo
        
    # creador de apoyos
    class Support:
        def __init__(self, support_type, pos):
            self.support_type = support_type   # pinned , roller
            self.pos = pos   # posición apoyo
            self.yreaction = None   # reacción en y
            
    # creador de cargas puntuales
    class point_Load:
        def __init__(self, pos, P, d):
            self.pos = pos   # posición carga
            self.P = P   # magnitud carga
            self.d = d   # dirección carga ('up' o 'down')
    
    # creador de cargas distribuídas
    class distributed_Load:
        def __init__(self, start_pos, end_pos, P, d):
            self.start_pos = start_pos
            self.end_pos = end_pos
            self.P = P
            self.d = d
            
    # agregar apoyos
    def add_support(self, support_type, pos):
        self.supports.append(self.Support(support_type, pos))
        self.nodes.append(self.Node('support', pos))
        
    # agregar carga puntual
    def add_point_load(self, pos, P, d):
        if d == 'down':
            P = -P   # signo carga (positivo hacia arriba, negativo hacia abajo)
        self.loads.append([self.point_Load(pos, P, d), 'point'])
        self.nodes.append(self.Node('load', pos))
        
    # agregar carga distribuída
    def add_distributed_load(self, start_pos, end_pos, P, d):
        if d == 'down':
            P = -P   # signo carga (positivo hacia arriba, negativo hacia abajo)
        self.loads.append([self.distributed_Load(start_pos, end_pos, P, d), 'distributed'])
        
    # calcular cargas equivalentes
    def equivalent_loads(self):
        for load in self.loads:
            if load[1] == 'point':
                self.eq_loads.append(load[0])
            elif load[1] == 'distributed':
                pos = (load[0].start_pos + load[0].end_pos)/2
                P = load[0].P * (load[0].end_pos - load[0].start_pos)
                self.eq_loads.append(self.point_Load(pos, P, load[0].d))
                self.nodes.append(self.Node('load', pos))
        
    # calcular reacciones
    def reactions(self):
        self.equivalent_loads()
        
        sum_loads = sum([load.P for load in self.eq_loads])
        By = -sum([load.P * load.pos for load in self.eq_loads])/self.supports[1].pos   # Despejamos By en la ecuación de momento respecto a A.
        Ay = -sum_loads - By
        self.supports[0].yreaction = Ay
        self.supports[1].yreaction = By
            
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
                node.load = self.eq_loads[load_id].P
                load_id += 1
    
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
            
        def drawSupports(support):
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
    
    # dibujar cargas    
    def draw_loads(self):
        for load in self.loads:
            if load[1] == 'point':
                arrow_h = self.L/6.8
                arrow_w = self.L/170
                head_w = self.L/(17/0.35)
                text_dy = arrow_h + arrow_h/4
                if load[0].d == 'down':
                    ax.arrow(load[0].pos, arrow_h, 0, -arrow_h, width=arrow_w, head_width=head_w, length_includes_head=True, color='black', linewidth=0.5)
                    ax.text(load[0].pos, text_dy, f'{abs(load[0].P)} kN', horizontalalignment='center', verticalalignment='center', fontsize=8)
            else:
                arrow_h = self.L/9.5
                arrow_w = self.L/380
                head_w = self.L/80
                text_dy = arrow_h + arrow_h/4
                dist = load[0].end_pos - load[0].start_pos
                mid_pos = (load[0].start_pos + load[0].end_pos)/2
                if load[0].d == 'down':
                    if isinstance(dist, int):
                        for i in range(load[0].start_pos, load[0].end_pos + 1):
                            ax.arrow(i, arrow_h, 0, -arrow_h, width=arrow_w, head_width=head_w, length_includes_head=True, color='black', linewidth=0.5)
                    ax.hlines(y=arrow_h, xmin=load[0].start_pos, xmax=load[0].end_pos, color='black', linewidth=1.3)
                    ax.text(mid_pos, text_dy, f'{abs(load[0].P)} kN$\cdot$m', horizontalalignment='center', verticalalignment='center', fontsize=8)
                
    # dibujar reacciones
    def draw_reactions(self):
        for support in self.supports:
            arrow_h = self.L/8.5
            arrow_w = self.L/170
            head_w = self.L/(17/0.35)
            text_dy = arrow_h + arrow_h/4
            if support.yreaction > 0:
                ax.arrow(support.pos, -arrow_h, 0, arrow_h, width=arrow_w, head_width=head_w, length_includes_head=True, facecolor='red', linewidth=0.5)
                ax.text(support.pos, -text_dy, f'{round(abs(support.yreaction), 2)} kN', horizontalalignment='center', verticalalignment='center', fontsize=8)
            elif support.yreaction < 0:
                ax.arrow(support.pos, arrow_h, 0, -arrow_h, width=arrow_w, head_width=head_w, length_includes_head=True, facecolor='red', linewidth=0.5)
                ax.text(support.pos, text_dy, f'{round(abs(support.yreaction), 2)} kN', horizontalalignment='center', verticalalignment='center', fontsize=8)
                
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
    def draw_beam_all(self):
        self.reactions()
        self.draw_beam()
        self.draw_supports()
        self.draw_loads()
        self.draw_reactions()
        plt.axis('equal')
        plt.show()
                

v = Beam(10)
v.add_support('pinned', 0)
v.add_support('roller', v.L)
v.add_distributed_load(2, 5, 3, 'down')
v.add_distributed_load(7, 9, 8, 'down')
v.add_point_load(4.5, 7, 'down')

fig, ax = plt.subplots()

# no mostrar ejes
ax.yaxis.set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

v.draw_beam_all()