import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
from constructores.Node import Node
from constructores.Element import Element
from constructores.Support import Support
from constructores.PointLoad import PointLoad
from constructores.DistributedLoad import DistributedLoad
from constructores.TriangularLoad import TriangularLoad


fig, ax = plt.subplots()
# no mostrar ejes
ax.yaxis.set_visible(False)
ax.spines["left"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
# ajustar tamaño de ticks
ax.tick_params(axis="x", labelsize=8)
ax.tick_params(axis="y", labelsize=8)


# creador de viga
class Beam:
    def __init__(self, L):
        self.L = L  # largo viga
        self.node_id = 1  # contador node id
        self.nodes = []  # [Node] lista con nodos
        self.eq_nodes = []  # [Node] lista con nodos equivalentes
        self.supports = []  # [Support] lista con apoyos
        self.cargas = []  # [Load] lista con cargas
        self.eq_cargas = []  # [Load] lista con cargas transformadas a puntuales
        self.forces = []  # [Load] lista con todas las fuerzas (cargas y reacciones)
        self.eq_forces = []  # [Load] lista con todas la fuerzas equivalentes en cargas puntuales
        self.reactions_count = 0  # contador reactions()
        self.calculate_count = 0  # contador calculate()
        self.elements = []  # [Element] lista con elementos

    # agregar apoyos
    def add_support(self, support_type, pos):
        if pos < 0 or pos > self.L: print(f"\n! Error: Posición incorrecta para apoyo en posición {pos}.\n")
        else:
            objeto = Support(support_type, pos, self.node_id)
            self.supports.append(objeto)
            self.nodes.append(Node("support", pos, self.node_id, objeto))
            self.node_id += 1
        if len(self.supports) > 1 and any(support.type == 'fixed' for support in self.supports): print('\n! Error: Hay más reacciones que ecuaciones.\n')

    # agregar carga puntual
    def add_point_load(self, pos, load, d="down"):
        if d == "down":
            load = -load  # signo carga (positivo hacia arriba, negativo hacia abajo)
        objeto = PointLoad(pos, load, d, self.node_id)
        self.cargas.append(objeto)
        self.nodes.append(Node("point_load", pos, self.node_id, objeto))
        self.node_id += 1

    # agregar carga distribuida
    def add_distributed_load(self, start_pos, end_pos, load, d="down"):
        if d == "down":
            load = -load  # signo carga (positivo hacia arriba, negativo hacia abajo)
        objeto = DistributedLoad(start_pos, end_pos, load, d, [self.node_id, self.node_id + 1])
        self.cargas.append(objeto)
        self.nodes.append(Node("distributed_load_L", start_pos, self.node_id, objeto))
        self.node_id += 1
        self.nodes.append(Node("distributed_load_R", end_pos, self.node_id, objeto))
        self.node_id += 1

    # agregar carga triangular simple
    def add_triangular_load(self, start_pos, end_pos, load, a_d, d="down"):
        if d == "down":
            load = -load  # signo carga (positivo hacia arriba, negativo hacia abajo)
        objeto = TriangularLoad(start_pos, end_pos, load, a_d, d, [self.node_id, self.node_id + 1])
        self.cargas.append(objeto)
        if a_d == "ascending":
            self.nodes.append(Node("triangular_load_min", start_pos, self.node_id, objeto))
            self.node_id += 1
            self.nodes.append(Node("triangular_load_max", end_pos, self.node_id, objeto))
            self.node_id += 1
        elif a_d == "descending":
            self.nodes.append(Node("triangular_load_max", start_pos, self.node_id, objeto))
            self.node_id += 1
            self.nodes.append(Node("triangular_load_min", end_pos, self.node_id, objeto))
            self.node_id += 1

    # calcular cargas equivalentes
    def equivalent_loads(self):
        for carga in self.cargas:
            if type(carga).__name__ == "PointLoad":
                self.eq_cargas.append(carga)
            elif type(carga).__name__ == "DistributedLoad":
                load = carga.load * carga.length
                self.eq_cargas.append(PointLoad(carga.pos, load, carga.d, self.node_id))
            elif type(carga).__name__ == "TriangularLoad":
                load = (carga.load * carga.length) / 2
                self.eq_cargas.append(PointLoad(carga.pos, load, carga.d, self.node_id))

    # calcular reacciones
    def reactions(self):
        if self.reactions_count < 1:
            self.equivalent_loads()

            sum_loads = sum([carga.load for carga in self.eq_cargas])
            By = -sum([carga.load * carga.pos for carga in self.eq_cargas]) / self.supports[1].pos  # Despejamos By en la ecuación de momento respecto a A.
            Ay = -sum_loads - By
            self.supports[0].yreaction = Ay
            self.supports[1].yreaction = By

            self.supports = sorted(self.supports, key=lambda x: x.pos)  # ordenar apoyos por posición

            self.reactions_count += 1
        else:
            pass

    # almacenar todas las cargas en nodos
    def calculate(self):
        if self.calculate_count < 1:
            self.reactions()

            def UpDown(support):
                if support.yreaction > 0:
                    return "up"
                else:
                    return "down"

            [self.forces.append(carga) for carga in self.cargas]
            [self.forces.append(PointLoad(support.pos, support.yreaction, UpDown(support), support.node_id)) for support in self.supports]
            self.forces = sorted(self.forces, key=lambda x: x.pos)  # ordenar fuerzas por posición

            self.nodes = sorted(self.nodes, key=lambda x: x.pos)  # ordenar nodos por posición
            for node in self.nodes:
                if node.type == "support":
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
                if type(force).__name__ == "DistributedLoad":
                    load = force.load * force.length
                    self.eq_forces.append(PointLoad(force.pos, load))
                elif type(force).__name__ == "TriangularLoad":
                    load = (force.load * force.length) / 2
                    self.eq_forces.append(PointLoad(force.pos, load))
                else:
                    self.eq_forces.append(force)

            # nodos equivalentes (por si hay dos nodos en la misma posición)
            for _ in range(len(self.nodes)):
                for i in range(len(self.nodes) - 1):
                    if self.nodes[i].pos == self.nodes[i + 1].pos:
                        if self.nodes[i].type == "support":
                            if self.nodes[i + 1].type == "point_load":
                                load1 = self.nodes[i].load
                                load2 = self.nodes[i + 1].load
                                self.nodes[i] = Node("support_load", self.nodes[i].pos, self.nodes[i].id, [self.nodes[i].objeto, self.nodes[i + 1].objeto])
                                self.nodes[i].load = [load1, load2]
                                self.nodes.pop(i + 1)
                                break

            # asignar el número de cargas en cada nodo
            for node in self.nodes:
                if type(node.load) == list:
                    node.load_num = 2
                else:
                    node.load_num = 1
                    
            # asignar carga neta en cada nodo
            for node in self.nodes:
                if node.load_num > 1:
                    node.load_neta = sum(node.load)
                else:
                    node.load_neta = node.load

            # agregar elementos a lista elements
            elements_num = len(self.nodes) - 1
            for i in range(elements_num):
                self.elements.append(Element(self.nodes[i], self.nodes[i + 1]))

            # calcular el valor que se le restará a x al calcular el momento
            suma = 0
            for i in range(1, elements_num):
                suma += self.elements[i - 1].length
                self.elements[i].subx = suma

            self.calculate_count += 1
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

        V = []
        eqV = []
        ejeX = []

        for i in range(len(self.elements)):
            node = self.nodes[i]
            element = self.elements[i]
            tramoX = tramosX[i]
            tramoX_ex = tramosX_ex[i]
            x = sp.Symbol("x")

            if node.type == "point_load" or node.type == "support" or node.type == "support_load":
                eq = node.load_neta
                eqV.append(eq)
                eqV_sum = sum(eqV)
                for X in tramoX:
                    V.append(eqV_sum)
                    ejeX.append(X)

            elif node.type == "distributed_load_L":
                eq = node.load_neta * (x - element.subx)
                eqV.append(eq)
                eqV_sum = sum(eqV)
                for X in tramoX:
                    V.append(eqV_sum.subs(x, X))
                    ejeX.append(X)
                eqV[-1] = eq.subs(x, X)

            elif node.type == "distributed_load_R":
                eqV_sum = sum(eqV)
                for X in tramoX:
                    V.append(eqV_sum)
                    ejeX.append(X)

            elif node.type == "triangular_load_min":
                if node.objeto.a_d == "ascending":
                    base = x - element.subx
                    w = (node.load_neta / element.length) * base  # calcular razón entre triángulos para obtener la altura en términos de x (ver info.md)
                    eq = (w * base) / 2
                    eqV.append(eq)
                    eqV_sum = sum(eqV)
                    for X in tramoX_ex:
                        V.append(eqV_sum.subs(x, X))
                        ejeX.append(X)
                    eqV[-1] = eq.subs(x, X)

                elif node.objeto.a_d == "descending":
                    eqV_sum = sum(eqV)
                    for X in tramoX:
                        V.append(eqV_sum)
                        ejeX.append(X)

            elif node.type == "triangular_load_max":
                if node.objeto.a_d == "descending":
                    base = x - element.subx
                    h = (node.load_neta / element.length) * base
                    k = node.load_neta - h
                    triangulo = (h * base) / 2
                    cuadrado = k * base
                    eq = triangulo + cuadrado
                    eqV.append(eq)
                    eqV_sum = sum(eqV)
                    for X in tramoX_ex:
                        V.append(eqV_sum.subs(x, X))
                        ejeX.append(X)
                    eqV[-1] = eq.subs(x, X)

                elif node.objeto.a_d == "ascending":
                    eqV_sum = sum(eqV)
                    for X in tramoX:
                        V.append(eqV_sum)
                        ejeX.append(X)

        return V, ejeX

    # calcular momento flector
    def bending_moment(self):
        self.calculate()
        tramosX, tramosX_ex, tramos, eje_x, x_ex = self.tramos()

        M = []
        eqM = []

        for i in range(len(self.elements)):
            node = self.nodes[i]
            element = self.elements[i]
            tramo = tramosX_ex[i]
            x = sp.Symbol("x")

            if node.type == "point_load" or node.type == "support" or node.type == "support_load":
                eq = node.load_neta * (x - element.subx)
                eqM.append(eq)
                eqM_sum = sum(eqM)
                for X in tramo:
                    M.append(eqM_sum.subs(x, X))

            elif node.type == "distributed_load_L":
                eq = node.load_neta * (x - element.subx) * ((x - element.subx) / 2)
                eqM.append(eq)
                eqM_sum = sum(eqM)
                for X in tramo:
                    M.append(eqM_sum.subs(x, X))
                new_last_eq = node.load_neta * (x - element.subx)
                eqM[-1] = new_last_eq.subs(x, X)

            elif node.type == "distributed_load_R":
                eq = eqM[-1] * (x - (self.elements[i - 1].subx + (self.elements[i - 1].length / 2)))
                eqM.pop()
                eqM.append(eq)
                eqM_sum = sum(eqM)
                for X in tramo:
                    M.append(eqM_sum.subs(x, X))

            elif node.type == "triangular_load_min":
                if node.objeto.a_d == "ascending":
                    base = x - element.subx
                    w = (node.load_neta / element.length) * base
                    eq = ((w * base) / 2) * ((1 / 3) * base)
                    eqM.append(eq)
                    eqM_sum = sum(eqM)
                    for X in tramo:
                        M.append(eqM_sum.subs(x, X))
                    new_last_eq = (node.load_neta * (x - element.subx)) / 2
                    eqM[-1] = new_last_eq.subs(x, X)

                elif node.objeto.a_d == "descending":
                    eq = eqM[-1] * (x - (self.elements[i - 1].subx + (self.elements[i - 1].length * (1 / 3))))
                    eqM.pop()
                    eqM.append(eq)
                    eqM_sum = sum(eqM)
                    for X in tramo:
                        M.append(eqM_sum.subs(x, X))

            elif node.type == "triangular_load_max":
                if node.objeto.a_d == "descending":
                    base = x - element.subx
                    h = (node.load_neta / element.length) * base
                    k = node.load_neta - h
                    triangulo = ((h * base) / 2) * ((2 / 3) * base)
                    cuadrado = (k * base) * (base / 2)
                    eq = triangulo + cuadrado
                    eqM.append(eq)
                    eqM_sum = sum(eqM)
                    for X in tramo:
                        M.append(eqM_sum.subs(x, X))
                    new_last_eq = (node.load_neta * (x - element.subx)) / 2
                    eqM[-1] = new_last_eq.subs(x, X)

                elif node.objeto.a_d == "ascending":
                    eq = eqM[-1] * (x - (self.elements[i - 1].subx + (self.elements[i - 1].length * (2 / 3))))
                    eqM.pop()
                    eqM.append(eq)
                    eqM_sum = sum(eqM)
                    for X in tramo:
                        M.append(eqM_sum.subs(x, X))

        return M

    # artistas de viga
    # definir xticks
    def newTicks(self, coords=None, decimals=3):
        if coords is not None:
            ax.set_xticks([coords[0]])
            ax.set_yticks([coords[1]])
            ax.xaxis.set_major_formatter(plt.FormatStrFormatter(f"%.{decimals}f"))
            ax.yaxis.set_major_formatter(plt.FormatStrFormatter(f"%.{decimals}f"))
        else:
            ticks = []
            for node in self.nodes:
                ticks.append(node.pos)
            ax.set_xticks(ticks)

    # dibujar viga
    def draw_beam(self):
        ax.hlines(y=0, xmin=0, xmax=self.L, color="#000000", linewidth=3)

    # dibujar nodos
    def draw_nodes(self):
        for node in self.nodes:
            ax.scatter(node.pos, 0, s=20, c="#FFD500", marker="s", linewidths=0.5, edgecolors="#000000", zorder=2)

    # dibujar linea en nodos
    def draw_node_lines(self):
        for node in self.nodes:
            ax.axvline(x=node.pos, ymax=0.5, color="#909090", linestyle="--", linewidth=0.5, dashes=(4, 3), zorder=0)

    # dibujar apoyos
    def draw_supports(self):
        l = self.L / 34  # real = 2*l   # longitud apoyo
        h = self.L / 17  # altura apoyo

        # dibujar sub-apoyo (sombra)
        def sub_support(pos):
            sub_l = l + l * 0.35  # longitud sub-apoyo
            sub_h = h + l * 0.45  # altura sub-apoyo
            ax.hlines(y=-h, xmin=pos - sub_l, xmax=pos + sub_l, color="#000000")
            ax.fill((pos - sub_l, pos + sub_l, pos + sub_l, pos - sub_l), (-h, -h, -sub_h, -sub_h), color="#CBCBCB")

        def drawSupports(support):
            if support.type == "pinned":
                ax.fill((support.pos - l, support.pos + l, support.pos, support.pos - l), (-h, -h, 0, -h), color="#264F92")
                sub_support(support.pos)
            elif support.type == "roller":
                r = self.L / 85
                ax.fill((support.pos - l, support.pos + l, support.pos, support.pos - l), (-(h - 2 * r), -(h - 2 * r), 0, -(h - 2 * r)), color="#264F92")
                circle1 = plt.Circle((support.pos - (l - r), -(h - r)), r, color="#264F92")
                circle2 = plt.Circle((support.pos + (l - r), -(h - r)), r, color="#264F92")
                ax.add_artist(circle1)
                ax.add_artist(circle2)
                sub_support(support.pos)

        for support in self.supports:
            drawSupports(support)

    # dibujar reacciones
    def draw_reactions(self, decimals=2):
        for support in self.supports:
            arrow_h = self.L / 8.5
            arrow_w = self.L / 170
            head_w = self.L / (17 / 0.35)
            text_dy = arrow_h + arrow_h / 5
            if support.yreaction > 0:
                ax.arrow(support.pos, -arrow_h, 0, arrow_h, width=arrow_w, head_width=head_w, length_includes_head=True, facecolor="#FF0000", linewidth=0.5, zorder=3)
                ax.text(support.pos, -text_dy, f"{round(abs(support.yreaction), decimals)} kN", horizontalalignment="center", verticalalignment="center", fontsize=6, zorder=3)
            elif support.yreaction < 0:
                ax.arrow(support.pos, arrow_h, 0, -arrow_h, width=arrow_w, head_width=head_w, length_includes_head=True, facecolor="#FF0000", linewidth=0.5, zorder=3)
                ax.text(support.pos, text_dy, f"{round(abs(support.yreaction), decimals)} kN", horizontalalignment="center", verticalalignment="center", fontsize=6, zorder=3)

    # dibujar cargas
    def draw_loads(self):
        for carga in self.cargas:
            # dibujar carga puntual
            if type(carga).__name__ == "PointLoad":
                arrow_h = self.L / 6.8
                arrow_w = self.L / 250
                head_w = self.L / 60
                text_dy = arrow_h + arrow_h / 5
                if carga.d == "down":
                    ax.arrow(carga.pos, arrow_h, 0, -arrow_h, width=arrow_w, head_width=head_w, length_includes_head=True, color="#000000", linewidth=0.5, zorder=3)
                    ax.text(carga.pos, text_dy, f"{abs(carga.load)} kN", horizontalalignment="center", verticalalignment="center", fontsize=6, zorder=3)
            # dibujar carga distribuida
            elif type(carga).__name__ == "DistributedLoad":
                arrow_h = self.L / 9.5
                arrow_w = self.L / 380
                head_w = self.L / 80
                text_dy = arrow_h + arrow_h / 4
                mid_pos = (carga.start_pos + carga.end_pos) / 2
                if carga.d == "down":
                    if isinstance(carga.length, int):
                        for i in range(carga.start_pos, carga.end_pos + 1):
                            ax.arrow(i, arrow_h, 0, -arrow_h, width=arrow_w, head_width=head_w, length_includes_head=True, color="#000000", linewidth=0.5, zorder=3)
                        ax.hlines(y=arrow_h, xmin=carga.start_pos, xmax=carga.end_pos, color="#000000", linewidth=1.3, zorder=3)
                        ax.text(mid_pos, text_dy, f"{abs(carga.load)} kN/m", horizontalalignment="center", verticalalignment="center", fontsize=6, zorder=3)
            # dibujar carga triangular
            elif type(carga).__name__ == "TriangularLoad":
                arrow_h = self.L / 9.5
                h_factor = arrow_h / carga.length
                arrow_w = self.L / 380
                head_w = self.L / 80
                text_dy = arrow_h + arrow_h / 4
                if isinstance(carga.length, int):
                    if carga.a_d == "ascending":
                        h = 0
                        for i in range(carga.start_pos, carga.end_pos + 1):
                            ax.arrow(i, h, 0, -h, width=arrow_w, head_width=head_w, length_includes_head=True, color="#000000", linewidth=0.5, zorder=3)
                            h += h_factor
                        ax.plot((carga.start_pos, carga.end_pos), (0, arrow_h), color="#000000", linewidth=1.3, zorder=3)
                        ax.text(carga.end_pos, text_dy, f"{abs(carga.load)} kN/m", horizontalalignment="center", verticalalignment="center", fontsize=6, zorder=3)
                    elif carga.a_d == "descending":
                        h = arrow_h
                        for i in range(carga.start_pos, carga.end_pos + 1):
                            ax.arrow(i, h, 0, -h, width=arrow_w, head_width=head_w, length_includes_head=True, color="#000000", linewidth=0.5, zorder=3)
                            h -= h_factor
                        ax.plot((carga.start_pos, carga.end_pos), (arrow_h, 0), color="#000000", linewidth=1.3, zorder=3)
                        ax.text(carga.start_pos, text_dy, f"{abs(carga.load)} kN/m", horizontalalignment="center", verticalalignment="center", fontsize=6, zorder=3)

    # dibujar solicitado
    def draw_beam_elements(self, solicitado, nodes=False, load_lines=False, decimals=2):  # solicitado = ['beam', 'supports', 'loads', 'reactions']
        self.reactions()
        for artist in solicitado:
            if artist == "beam":
                self.draw_beam()
            elif artist == "supports":
                self.draw_supports()
            elif artist == "loads":
                self.draw_loads()
            elif artist == "reactions":
                self.draw_reactions(decimals=decimals)
        if nodes == True:
            self.draw_nodes()
        if load_lines == True:
            self.draw_load_lines()
            self.newTicks()
        if solicitado == ["beam"]:
            plt.show()
        else:
            plt.axis("equal")
            plt.show()

    # dibujar todos los elementos de la viga
    def draw_beam_all(self, nodes=False, load_lines=True, decimals=2):
        self.reactions()
        self.draw_beam()
        self.draw_supports()
        self.draw_loads()
        self.draw_reactions(decimals=decimals)
        if load_lines == True:
            self.draw_node_lines()
            self.newTicks()
        if nodes == True:
            self.draw_nodes()
        plt.axis("equal")
        plt.show()

    # artistas diagramas
    # dibujar diagrama de fuerza cortante
    def draw_shear(self, nodes=False):
        V, x = self.shear_force()

        x = np.array(x, dtype=float)
        V = np.array(V, dtype=float)

        ax.plot(x, V)
        ax.fill_between(x, V, color="#328DCB", alpha=0.4)

        y_max = max(abs(np.asarray(V)))
        ax.set_ylim(-(y_max * 2), (y_max * 2))

        ax.yaxis.set_visible(True)
        ax.spines["left"].set_visible(True)
        ax.grid(linewidth=0.2)  # cuadrícula
        ax.minorticks_on()  # sub valores ejes
        ax.grid(linewidth=0.1, which="minor", linestyle=":")  # sub cuadrícula
        ax.set_axisbelow(True)  # cuadrícula detrás de la gráfica
        ax.set_title("Diagrama de fuerza cortante")

        if nodes == True:
            self.draw_nodes()
        self.draw_beam_elements(["beam"])

    # dibujar diagrama de momento flector
    def draw_moment(self, nodes=False, max_value=False, decimals=3):
        M = self.bending_moment()
        tramosX, tramosX_ex, tramos, x, x_ex = self.tramos()

        x_ex = np.array(x_ex, dtype=float)
        M = np.array(M, dtype=float)

        ax.plot(x_ex, M)
        ax.fill_between(x_ex, M, color="#328DCB", alpha=0.4)

        y_max = max(abs(np.asarray(M)))
        ax.set_ylim(-(y_max * 2), (y_max * 2))

        ax.yaxis.set_visible(True)
        ax.spines["left"].set_visible(True)
        ax.grid(linewidth=0.2)  # cuadrícula
        ax.minorticks_on()  # sub valores ejes
        ax.grid(linewidth=0.1, which="minor", linestyle=":")  # sub cuadrícula
        ax.set_axisbelow(True)  # cuadrícula detrás de la gráfica
        ax.set_title("Diagrama de momento flector")

        if max_value == True:
            indice_max_M, valor_max_M = max(enumerate(M), key=lambda x: x[1])
            x_max = x_ex[indice_max_M]
            M_max = valor_max_M
            ax.scatter(x_max, M_max, s=20, c="#FF0000", linewidth=0.6, edgecolor="#000000", zorder=3)  # zorder=3 porque ax.plot() tiene zorder=2 por defecto
            ax.axhline(y=M_max, color="#707070", linestyle="--", linewidth=0.6, zorder=2)
            ax.axvline(x=x_max, color="#707070", linestyle="--", linewidth=0.6, zorder=2)
            ax.grid(False)
            ax.minorticks_off()
            self.newTicks(coords=(x_max, M_max), decimals=decimals)

        if nodes == True:
            self.draw_nodes()
        self.draw_beam_elements(["beam"])
