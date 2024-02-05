# Caso hipotético: viga simplemente apoyada con cargas puntuales y distribuidas uniformes (no en los extremos)
# Calcula: reacciones | fuerza cortante | momento flector
# Dibuja: viga | apoyos | carga puntual | carga distribuida uniforme | reacciones | diagramas

import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

# creador de viga
class Beam:
    def __init__(self, L):
        self.L = L   # largo viga
        self.node_id = 1   # contador node id
        self.nodes = []   # [Node] lista con nodos
        self.eq_nodes = []   # [Node] lista con nodos equivalentes
        self.supports = []   # [Support] lista con apoyos
        self.cargas = []   # [Load] lista con cargas
        self.eq_cargas = []   # [Load] lista con cargas transformadas a puntuales
        self.forces = []   # [Load] lista con todas las fuerzas (cargas y reacciones)
        self.eq_forces = []   # [Load] lista con todas la fuerzas equivalentes en cargas puntuales
        self.calc_count = 0   # contador calculate()
        self.elements = [] # [Element] lista con elementos
        
    # creador de nodos
    class Node:
        def __init__(self, node_type, pos, node_id, objeto):
            self.type = node_type   # tipo de nodo ('support' , 'point_load' , 'distributed_load_L' , 'distributed_load_R' , 'support_load' , 'load_support)
            self.pos = pos   # posición nodo
            self.load = None   # carga en nodo
            self.load_num = None   # número de cargas en el nodo
            self.id = node_id   # id nodo
            self.objeto = objeto
            
    # creador de elementos
    class Element:
        def __init__(self, l_node, r_node, subx=0):
            self.l_node = l_node   # nodo en extremo izquierdo
            self.r_node = r_node   # nodo en extremo derecho
            self.length = r_node.pos - l_node.pos   # largo del elemento
            self.subx = subx   # número que se le restará a x al calcular el momento
        
    # creador de apoyos
    class Support:
        def __init__(self, support_type, pos, node_id):
            self.type = support_type   # pinned , roller
            self.pos = pos   # posición apoyo
            self.yreaction = None   # reacción en y
            self.node_id = node_id   # id nodo
            
    # creador de cargas puntuales
    class point_Load:
        def __init__(self, pos, load, d='down', node_id=None):
            self.type = 'point'
            self.pos = pos   # posición carga
            self.load = load   # magnitud carga
            self.d = d   # dirección carga ('up' o 'down')
            self.node_id = node_id   # id nodo
    
    # creador de cargas distribuidas
    class distributed_Load:
        def __init__(self, start_pos, end_pos, load, d='down', node_id=None):
            self.type = 'distributed'
            self.start_pos = start_pos   # posición inicial
            self.end_pos = end_pos   # posición final
            self.pos = (start_pos + end_pos)/2
            self.load = load   # magnitud carga
            self.d = d   # dirección carga ('up' o 'down')
            self.node_id = node_id   # id nodo
            
    # agregar apoyos
    def add_support(self, support_type, pos):
        objeto = self.Support(support_type, pos, self.node_id)
        self.supports.append(objeto)
        self.nodes.append(self.Node('support', pos, self.node_id, objeto))
        self.node_id += 1
        
    # agregar carga puntual
    def add_point_load(self, pos, load, d='down'):
        if d == 'down':
            load = -load   # signo carga (positivo hacia arriba, negativo hacia abajo)
        objeto = self.point_Load(pos, load, d, self.node_id)
        self.cargas.append(objeto)
        self.nodes.append(self.Node('point_load', pos, self.node_id, objeto))
        self.node_id += 1
        
    # agregar carga distribuida
    def add_distributed_load(self, start_pos, end_pos, load, d='down'):
        if d == 'down':
            load = -load   # signo carga (positivo hacia arriba, negativo hacia abajo)
        objeto = self.distributed_Load(start_pos, end_pos, load, d, [self.node_id, self.node_id+1])
        self.cargas.append(objeto)
        self.nodes.append(self.Node('distributed_load_L', start_pos, self.node_id, objeto))
        self.node_id += 1
        self.nodes.append(self.Node('distributed_load_R', end_pos, self.node_id, objeto))
        self.node_id += 1
        
    # calcular cargas equivalentes
    def equivalent_loads(self):
        for carga in self.cargas:
            if type(carga).__name__ == 'point_Load':
                self.eq_cargas.append(carga)
            elif type(carga).__name__ == 'distributed_Load':
                pos = (carga.start_pos + carga.end_pos)/2
                load = carga.load * (carga.end_pos - carga.start_pos)
                self.eq_cargas.append(self.point_Load(pos, load, carga.d, self.node_id))
        
    # calcular reacciones
    def reactions(self):
        self.equivalent_loads()
        
        sum_loads = sum([carga.load for carga in self.eq_cargas])
        By = -sum([carga.load * carga.pos for carga in self.eq_cargas])/self.supports[1].pos   # Despejamos By en la ecuación de momento respecto a A.
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
            
            [self.forces.append(carga) for carga in self.cargas]
            [self.forces.append(self.point_Load(support.pos, support.yreaction, UpDown(support), support.node_id)) for support in self.supports]
            self.forces = sorted(self.forces, key=lambda x: x.pos)   # ordenar fuerzas por posición
            
            self.nodes = sorted(self.nodes, key=lambda x: x.pos)   # ordenar nodos por posición
            for node in self.nodes:
                if node.type == 'support':
                    for support in self.supports:
                        if support.node_id == node.id:
                            node.load = support.yreaction
                else:
                    for carga in self.cargas:
                        if type(carga.node_id) == list:
                            if node.id in carga.node_id:
                                node.load = carga.load
                        else:
                            if node.id == carga.node_id:
                                node.load = carga.load
                
            # eq_forces: fuerzas equivalentes en cargas puntuales
            for force in self.forces:
                if type(force).__name__ == 'distributed_Load':
                    length = force.end_pos - force.start_pos
                    load = force.load * length
                    pos = (force.start_pos + force.end_pos)/2
                    self.eq_forces.append(self.point_Load(pos, load))
                else:
                    self.eq_forces.append(force)
                    
            # nodos equivalentes (por si hay dos nodos en la misma posición)
            iteraciones = len(self.nodes)
            for j in range(iteraciones):
                for i in range(len(self.nodes) - 1):
                    if self.nodes[i].pos == self.nodes[i+1].pos:
                        if self.nodes[i].type == 'support':
                            load1 = self.nodes[i].load
                            load2 = self.nodes[i+1].load
                            self.nodes[i] = self.Node('support_load', self.nodes[i].pos, self.nodes[i].id, [self.nodes[i].objeto, self.nodes[i+1].objeto])
                            self.nodes[i].load = [load1, load2]
                            self.nodes.pop(i + 1)
                            break
                        
            # asignar el número de cargas en cada nodo
            for node in self.nodes:
                if type(node.load) == list:
                    node.load_num = 2
                else:
                    node.load_num = 1
                
            # agregar elementos a lista elements
            elements_num = len(self.nodes) - 1  
            for i in range(elements_num):
                self.elements.append(self.Element(self.nodes[i], self.nodes[i+1])) 
                
            # calcular el valor que se le restará a x al calcular el momento
            suma = 0
            for i in range(1, elements_num):
                suma += self.elements[i-1].length
                self.elements[i].subx = suma
                    
            self.calc_count += 1
        else:
            pass
        
    # listas con tramos
    def tramos(self):
        self.calculate()

        tramosX = []
        n = 0
        for i in range(1, len(self.nodes)):
            node = self.nodes[i]
            lst = []
            for j in range(n, self.L + 1):
                lst.append(j)
                if node.pos == j:
                    tramosX.append(lst)
                    n = j
                    break
                
        x = []
        [x.extend(tramo) for tramo in tramosX]
                
        tramosX_ex = []
        for tramo in tramosX:
            a = tramo[0]
            b = tramo[-1]
            tramosX_ex.append(np.linspace(a, b, 100))
        
        x_ex = []
        [x_ex.extend(tramo) for tramo in tramosX_ex]
                
        tramos = []
        for tramo in tramosX:
            tramos.append(list(np.arange(len(tramo))))
                
        return tramosX, tramosX_ex, tramos, x, x_ex
        
    # calcular fuerza cortante
    def shear_force(self):
        self.calculate()
        tramosX, tramosX_ex, tramos, eje_x, x_ex = self.tramos()
        x = sp.Symbol('x')
        
        V = []
        eqV = []
        for i in range(len(self.elements)):
            node = self.nodes[i]
            element = self.elements[i]
            tramo = tramosX[i]
            
            if node.type == 'point_load' or node.type == 'support':
                eq = node.load
                eqV.append(eq)
                eqV_sum = sum(eqV)
                for j in range(len(tramo)):
                    V.append(eqV_sum)
                    
            elif node.type == 'distributed_load_L':
                eq = node.load * (x - element.subx)
                eqV.append(eq)
                eqV_sum = sum(eqV)
                for X in tramo:
                    v = eqV_sum.subs(x, X)
                    V.append(v)
                eqV[-1] = eq.subs(x, X)
                
            elif node.type == 'distributed_load_R':
                eqV_sum = sum(eqV)
                for j in range(len(tramo)):
                    V.append(eqV_sum)
                           
            else:
                pass
            
        return V
    
    # calcular momento flector
    def bending_moment(self):
        self.calculate()
        tramosX, tramosX_ex, tramos, eje_x, x_ex = self.tramos()
        x = sp.Symbol('x')
        
        M = []
        eqM = []
        for i in range(len(self.elements)):
            node = self.nodes[i]
            element = self.elements[i]
            tramo = tramosX_ex[i]

            if node.type == 'point_load' or node.type == 'support':
                m = node.load * (x - element.subx)
                eqM.append(m)
                eqM_sum = sum(eqM)
                for X in tramo:
                    M.append(eqM_sum.subs(x, X))
            
            elif node.type == 'distributed_load_L':
                m = node.load * (x - element.subx) * ((x - element.subx)/2)
                eqM.append(m)
                eqM_sum = sum(eqM)
                for X in tramo:
                    M.append(eqM_sum.subs(x, X))
                new_last_m = node.load * (x - element.subx)
                eqM[-1] = new_last_m.subs(x, X)
                
            elif node.type == 'distributed_load_R':
                m = eqM[-1] * (x - (self.elements[i-1].subx + (element.subx - self.elements[i-1].subx)/2))
                eqM.pop()
                eqM.append(m)
                eqM_sum = sum(eqM)
                for X in tramo:
                    M.append(eqM_sum.subs(x, X))
                    
            else:
                pass
            
        return M              
    
     
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
        for carga in self.cargas:
            if type(carga).__name__ == 'point_Load':
                arrow_h = self.L/6.8
                arrow_w = self.L/250
                head_w = self.L/60
                text_dy = arrow_h + arrow_h/4
                if carga.d == 'down':
                    ax.arrow(carga.pos, arrow_h, 0, -arrow_h, width=arrow_w, head_width=head_w, length_includes_head=True, color='black', linewidth=0.5, zorder=4)
                    ax.text(carga.pos, text_dy, f'{abs(carga.load)} kN', horizontalalignment='center', verticalalignment='center', fontsize=8, zorder=4)
            else:
                arrow_h = self.L/9.5
                arrow_w = self.L/380
                head_w = self.L/80
                text_dy = arrow_h + arrow_h/4
                dist = carga.end_pos - carga.start_pos
                mid_pos = (carga.start_pos + carga.end_pos)/2
                if carga.d == 'down':
                    if isinstance(dist, int):
                        for i in range(carga.start_pos, carga.end_pos + 1):
                            ax.arrow(i, arrow_h, 0, -arrow_h, width=arrow_w, head_width=head_w, length_includes_head=True, color='black', linewidth=0.5, zorder=4)
                    ax.hlines(y=arrow_h, xmin=carga.start_pos, xmax=carga.end_pos, color='black', linewidth=1.3, zorder=4)
                    ax.text(mid_pos, text_dy, f'{abs(carga.load)} kN$\cdot$m', horizontalalignment='center', verticalalignment='center', fontsize=8, zorder=4)
                
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
    # dibujar diagrama de fuerza cortante
    def draw_shear(self, nodes=False):
        V = self.shear_force()
        tramosX, tramosX_ex, tramos, x, x_ex = self.tramos()
        
        x = np.array(x, dtype=float)
        V = np.array(V, dtype=float)
        
        ax.plot(x, V)

        ax.fill_between(x, V, color='#328DCB', alpha=0.4)
        
        y_max = max(abs(np.asarray(V)))
        ax.set_ylim(-(y_max * 2), (y_max * 2))
        
        ax.yaxis.set_visible(True)
        ax.spines['left'].set_visible(True)
        ax.grid(linewidth=0.2)   # cuadrícula
        ax.minorticks_on()   # sub valores ejes
        ax.grid(linewidth=0.1, which='minor', linestyle=':')   # sub cuadrícula
        ax.set_axisbelow(True)   # cuadrícula detrás de la gráfica
        ax.set_title('Diagrama de fuerza cortante')
        
        if nodes == True:
            self.draw_nodes()
        self.draw_beam_elements(['beam'])
        
    # dibujar diagrama de momento flector
    def draw_moment(self, nodes=False):
        M = self.bending_moment()
        tramosX, tramosX_ex, tramos, x, x_ex = self.tramos()
        
        x_ex = np.array(x_ex, dtype=float)
        M = np.array(M, dtype=float)
        
        ax.plot(x_ex, M)

        ax.fill_between(x_ex, M, color='#328DCB', alpha=0.4)
        
        y_max = max(abs(np.asarray(M)))
        ax.set_ylim(-(y_max * 2), (y_max * 2))
        
        ax.yaxis.set_visible(True)
        ax.spines['left'].set_visible(True)
        ax.grid(linewidth=0.2)   # cuadrícula
        ax.minorticks_on()   # sub valores ejes
        ax.grid(linewidth=0.1, which='minor', linestyle=':')   # sub cuadrícula
        ax.set_axisbelow(True)   # cuadrícula detrás de la gráfica
        ax.set_title('Diagrama de fuerza cortante')
        
        if nodes == True:
            self.draw_nodes()
        self.draw_beam_elements(['beam'])
           


v = Beam(20)
v.add_support('pinned', 0) 
v.add_support('roller', v.L)
v.add_distributed_load(2, 5, 3)
v.add_point_load(7, 7.5)
v.add_distributed_load(8, 11, 3.2)
v.add_point_load(13, 4)
v.add_distributed_load(15, 19, 5)

fig, ax = plt.subplots()

# no mostrar ejes
ax.yaxis.set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

v.draw_moment()