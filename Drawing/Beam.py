import matplotlib.pyplot as plt
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
        w = self.L / 130  # ancho apoyo empotrado

        # dibujar sub-apoyo (sombra)
        def sub_support(pos, fixed=False):
            if fixed == True:
                sub_h = h + l * 0.35
                sub_l = w + l * 0.45
                if support.pos == 0:
                    ax.vlines(x=-w, ymin=-sub_h, ymax=sub_h, color="#000000")
                    ax.fill((-sub_l, -w, -w, -sub_l), (sub_h, sub_h, -sub_h, -sub_h), color="#CBCBCB")
                else:
                    ax.vlines(x=pos + w, ymin=-sub_h, ymax=sub_h, color="#000000")
                    ax.fill((pos + sub_l, pos + w, pos + w, pos + sub_l), (sub_h, sub_h, -sub_h, -sub_h), color="#CBCBCB")
            else:
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
            elif support.type == "fixed":
                if support.pos == 0:
                    ax.fill((support.pos - w, support.pos, support.pos, support.pos - w), (h, h, -h, -h), color="#264F92")
                    sub_support(support.pos, fixed=True)
                else:
                    ax.fill((support.pos + w, support.pos, support.pos, support.pos + w), (h, h, -h, -h), color="#264F92")
                    sub_support(support.pos, fixed=True)

        for support in self.supports:
            drawSupports(support)

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
        for artist in solicitado:
            if artist == "beam":
                self.draw_beam()
            elif artist == "supports":
                self.draw_supports()
            elif artist == "loads":
                self.draw_loads()
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
        self.draw_beam()
        self.draw_supports()
        self.draw_loads()
        if load_lines == True:
            self.draw_node_lines()
            self.newTicks()
        if nodes == True:
            self.draw_nodes()
        plt.axis("equal")
        plt.show()