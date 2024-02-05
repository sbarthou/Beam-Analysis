# Caso hipotético: viga simplemente apoyada con cargas puntuales y/o distribuidas uniformes
# Calcula: reacciones | fuerza cortante
# Dibuja: viga | apoyos | carga puntual | carga distribuida uniforme | reacciones | diagrama fuerza cortante

import numpy as np
import matplotlib.pyplot as plt

# creador de viga
class Beam:
    def __init__(self, L):
        self.L = L   # largo viga
        self.node_id = 1   # contador node id
        self.nodes = []   # [Node] lista con nodos
        self.supports = []   # [Support] lista con apoyos
        self.loads = []   # [Load] lista con cargas
        self.eq_loads = []   # [Load] lista con cargas transformadas a puntuales
        self.forces = []   # [Load] lista con todas las fuerzas (cargas y reacciones)
        self.calc_count = 0   # contador calculate()
        
    # creador de nodos
    class Node:
        def __init__(self, node_type, pos, node_id):
            self.type = node_type   # tipo de nodo ('support' , 'point_load' , 'distributed_load_L' , 'distributed_load_R')
            self.pos = pos   # posición nodo
            self.load = None   # carga en nodo 
            self.id = node_id   # id nodo
        
    # creador de apoyos
    class Support:
        def __init__(self, support_type, pos, node_id):
            self.type = support_type   # pinned , roller
            self.pos = pos   # posición apoyo
            self.yreaction = None   # reacción en y
            self.node_id = node_id   # id nodo
            
    # creador de cargas puntuales
    class point_Load:
        def __init__(self, pos, P, d, node_id):
            self.type = 'point'
            self.pos = pos   # posición carga
            self.P = P   # magnitud carga
            self.d = d   # dirección carga ('up' o 'down')
            self.node_id = node_id   # id nodo
    
    # creador de cargas distribuidas
    class distributed_Load:
        def __init__(self, start_pos, end_pos, P, d, node_id):
            self.type = 'distributed'
            self.start_pos = start_pos   # posición inicial
            self.end_pos = end_pos   # posición final
            self.pos = (start_pos + end_pos)/2
            self.P = P   # magnitud carga
            self.d = d   # dirección carga ('up' o 'down')
            self.node_id = node_id   # id nodo
            
    # agregar apoyos
    def add_support(self, support_type, pos):
        self.supports.append(self.Support(support_type, pos, self.node_id))
        self.nodes.append(self.Node('support', pos, self.node_id))
        self.node_id += 1
        
    # agregar carga puntual
    def add_point_load(self, pos, P, d):
        if d == 'down':
            P = -P   # signo carga (positivo hacia arriba, negativo hacia abajo)
        self.loads.append(self.point_Load(pos, P, d, self.node_id))
        self.nodes.append(self.Node('point_load', pos, self.node_id))
        self.node_id += 1
        
    # agregar carga distribuida
    def add_distributed_load(self, start_pos, end_pos, P, d):
        if d == 'down':
            P = -P   # signo carga (positivo hacia arriba, negativo hacia abajo)
        self.loads.append(self.distributed_Load(start_pos, end_pos, P, d, [self.node_id, self.node_id+1]))
        self.nodes.append(self.Node('distributed_load_L', start_pos, self.node_id))
        self.node_id += 1
        self.nodes.append(self.Node('distributed_load_R', end_pos, self.node_id))
        self.node_id += 1
        
    # calcular cargas equivalentes
    def equivalent_loads(self):
        for load in self.loads:
            if type(load).__name__ == 'point_Load':
                self.eq_loads.append(load)
            elif type(load).__name__ == 'distributed_Load':
                pos = (load.start_pos + load.end_pos)/2
                P = load.P * (load.end_pos - load.start_pos)
                self.eq_loads.append(self.point_Load(pos, P, load.d, self.node_id))
        
    # calcular reacciones
    def reactions(self):
        self.equivalent_loads()
        
        sum_loads = sum([load.P for load in self.eq_loads])
        By = -sum([load.P * load.pos for load in self.eq_loads])/self.supports[1].pos   # Despejamos By en la ecuación de momento respecto a A.
        Ay = -sum_loads - By
        self.supports[0].yreaction = Ay
        self.supports[1].yreaction = By
            
        self.supports = sorted(self.supports, key=lambda x: x.pos)   # ordenar apoyos por posición
        
    # almacenar todas las cargas en nodos
    def calculate(self):
        if self.calc_count < 1:
            self.reactions()
            
            def UpDown(support):
                if support.yreaction > 0:
                    return 'up'
                else:
                    return 'down'
            
            [self.forces.append(load) for load in self.loads]
            [self.forces.append(self.point_Load(support.pos, support.yreaction, UpDown(support), support.node_id)) for support in self.supports]
            self.forces = sorted(self.forces, key=lambda x: x.pos)   # ordenar fuerzas por posición
            
            self.nodes = sorted(self.nodes, key=lambda x: x.pos)   # ordenar nodos por posición
            for node in self.nodes:
                if node.type == 'support':
                    for support in self.supports:
                        if support.node_id == node.id:
                            node.load = support.yreaction
                else:
                    for load in self.loads:
                        if type(load.node_id) == list:
                            if node.id in load.node_id:
                                node.load = load.P
                        else:
                            if node.id == load.node_id:
                                node.load = load.P
            self.calc_count += 1
        else:
            pass
        
        
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
            if support.type == 'pinned':
                ax.fill((support.pos-l, support.pos+l, support.pos, support.pos-l), (-h, -h, 0, -h), color='#264F92')
                sub_support(support.pos)
            elif support.type == 'roller':
                r = self.L/85
                ax.fill((support.pos-l, support.pos+l, support.pos, support.pos-l), (-(h-2*r), -(h-2*r), 0, -(h-2*r)), color='#264F92')
                circle1 = plt.Circle((support.pos-(l-r), -(h-r)), r, color='#264F92')
                circle2 = plt.Circle((support.pos+(l-r), -(h-r)), r, color='#264F92')
                ax.add_artist(circle1)
                ax.add_artist(circle2)
                sub_support(support.pos)
                
        for support in self.supports:
            drawSupports(support)
            
    # dibujar nodos
    def draw_nodes(self):
        for node in self.nodes:
            ax.scatter(node.pos, 0, s=20, c='#FFD500', marker='s', linewidths=0.5, edgecolors='black', zorder=3)
    
    # dibujar cargas    
    def draw_loads(self):
        for load in self.loads:
            if type(load).__name__ == 'point_Load':
                arrow_h = self.L/6.8
                arrow_w = self.L/250
                head_w = self.L/60
                text_dy = arrow_h + arrow_h/4
                if load.d == 'down':
                    ax.arrow(load.pos, arrow_h, 0, -arrow_h, width=arrow_w, head_width=head_w, length_includes_head=True, color='black', linewidth=0.5, zorder=4)
                    ax.text(load.pos, text_dy, f'{abs(load.P)} kN', horizontalalignment='center', verticalalignment='center', fontsize=8, zorder=4)
            else:
                arrow_h = self.L/9.5
                arrow_w = self.L/380
                head_w = self.L/80
                text_dy = arrow_h + arrow_h/4
                dist = load.end_pos - load.start_pos
                mid_pos = (load.start_pos + load.end_pos)/2
                if load.d == 'down':
                    if isinstance(dist, int):
                        for i in range(load.start_pos, load.end_pos + 1):
                            ax.arrow(i, arrow_h, 0, -arrow_h, width=arrow_w, head_width=head_w, length_includes_head=True, color='black', linewidth=0.5, zorder=4)
                    ax.hlines(y=arrow_h, xmin=load.start_pos, xmax=load.end_pos, color='black', linewidth=1.3, zorder=4)
                    ax.text(mid_pos, text_dy, f'{abs(load.P)} kN$\cdot$m', horizontalalignment='center', verticalalignment='center', fontsize=8, zorder=4)
                
    # dibujar reacciones
    def draw_reactions(self):
        for support in self.supports:
            arrow_h = self.L/8.5
            arrow_w = self.L/170
            head_w = self.L/(17/0.35)
            text_dy = arrow_h + arrow_h/4
            if support.yreaction > 0:
                ax.arrow(support.pos, -arrow_h, 0, arrow_h, width=arrow_w, head_width=head_w, length_includes_head=True, facecolor='red', linewidth=0.5, zorder=4)
                ax.text(support.pos, -text_dy, f'{round(abs(support.yreaction), 2)} kN', horizontalalignment='center', verticalalignment='center', fontsize=8, zorder=4)
            elif support.yreaction < 0:
                ax.arrow(support.pos, arrow_h, 0, -arrow_h, width=arrow_w, head_width=head_w, length_includes_head=True, facecolor='red', linewidth=0.5, zorder=4)
                ax.text(support.pos, text_dy, f'{round(abs(support.yreaction), 2)} kN', horizontalalignment='center', verticalalignment='center', fontsize=8, zorder=4)
                
    # dibujar solicitado
    def draw_beam_elements(self, solicitado, nodes=False):   # solicitado = ['beam', 'supports', 'loads', 'reactions']
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
        if nodes == True:
            self.draw_nodes()
        if solicitado == ['beam']:
            plt.show()
        else:
            plt.axis('equal')
            plt.show()
            
    # dibujar todos los elementos de la viga
    def draw_beam_all(self, nodes=False):
        self.reactions()
        self.draw_beam()
        self.draw_supports()
        self.draw_loads()
        self.draw_reactions()
        if nodes == True:
            self.draw_nodes()
        plt.axis('equal')
        plt.show()
        
        
    # artistas diagramas
    # lista con tramos
    def tramos(self):
        self.calculate()

        tramos_x = []
        n = 0
        for i in range(1, len(self.nodes)):
            node = self.nodes[i]
            lst = []
            for j in range(n, self.L + 1):
                lst.append(j)
                if node.pos == j:
                    tramos_x.append(lst)
                    n = j
                    break
                
        tramos = []
        for tramo in tramos_x:
            tramos.append(list(np.arange(len(tramo))))
                
        return tramos_x, tramos
    
    # dibujar diagrama de fuerza cortante
    def draw_shear(self):
        self.calculate()
        tramos_x, tramos = self.tramos()
        
        x = [0]
        [x.extend(tramo) for tramo in tramos_x]
        if self.forces[-1].pos == self.L:
            x.append(self.L)
        y = [0]
        
        V_forces = []
        for i in range(len(self.forces)):
            if self.forces[i].type == 'distributed':
                V_forces.append(self.forces[i])
                V_forces.append(0)
            else:
                V_forces.append(self.forces[i])
        
        for i in range(len(tramos)):
            tramo = tramos[i]
            load = V_forces[i]
            
            lst = []
            dy = y[-1]
            if load == 0:
                for X in tramo:
                    y_valor = dy
                    y.append(y_valor)
            else:
                if load.type == 'point':
                    for X in tramo:
                        y_valor = dy + load.P
                        y.append(y_valor)
                        lst.append(y_valor)
                else:
                    for X in tramo:
                        y_valor = dy + load.P*X
                        y.append(y_valor)
                        lst.append(y_valor)
        y.append(0)
        
        ax.plot(x, y)

        ax.fill_between(x, y, color='#328DCB', alpha=0.4)
        
        y_max = max(abs(np.asarray(y)))
        ax.set_ylim(-(y_max * 2), (y_max * 2))
        
        ax.yaxis.set_visible(True)
        ax.spines['left'].set_visible(True)
        ax.grid(linewidth=0.2)   # cuadrícula
        ax.minorticks_on()   # sub valores ejes
        ax.grid(linewidth=0.1, which='minor', linestyle=':')   # sub cuadrícula
        ax.set_axisbelow(True)   # cuadrícula detrás de la gráfica
        ax.set_title('Diagrama de fuerza cortante')
        
        self.draw_beam_elements(['beam'])




v = Beam(10)
v.add_support('pinned', 0)
v.add_support('roller', v.L)
v.add_distributed_load(0, 4, 5, 'down')
v.add_point_load(6, 15, 'down')
v.add_distributed_load(7, 8, 3, 'down')

fig, ax = plt.subplots()

# no mostrar ejes
ax.yaxis.set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

v.draw_shear()