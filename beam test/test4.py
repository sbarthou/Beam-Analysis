# Caso hipotético: viga simplemente apoyada con una carga puntual en el centro
# Calcula: reacciones
# Dibuja: viga | apoyos "pinned" o "roller" | carga puntual | reacciones

import matplotlib.pyplot as plt

# creador
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
    
    # artistas de viga
    
    # dibujar viga
    def draw_beam(self):
        ax.hlines(y=0, xmin=0, xmax=self.L, color='black', linewidth=3)
        
    # dibujar apoyos
    def draw_supports(self):
        l = v.L/34   # real = 2*l   # longitud apoyo
        h = v.L/17   # altura apoyo
        # dibujar sub-apoyo (sombra)    
        def sub_support(pos):   
            sub_l = l + l*0.35   # longitud sub-apoyo
            sub_h = h + l*0.45   # altura sub-apoyo
            ax.hlines(y=-h, xmin=pos-sub_l, xmax=pos+sub_l, color='black')
            ax.fill((pos-sub_l, pos+sub_l, pos+sub_l, pos-sub_l), (-h, -h, -sub_h, -sub_h), color='#CBCBCB')
            
        def draw(support):
            if support.support_type == 'pinned':
                ax.fill((support.pos-l, support.pos+l, support.pos, support.pos-l), (-h, -h, 0, -h), color='#264F92')
                sub_support(support.pos)
            elif support.support_type == 'roller':
                r = v.L/85
                ax.fill((support.pos-l, support.pos+l, support.pos, support.pos-l), (-(h-2*r), -(h-2*r), 0, -(h-2*r)), color='#264F92')
                circle1 = plt.Circle((support.pos-(l-r), -(h-r)), r, color='#264F92')
                circle2 = plt.Circle((support.pos+(l-r), -(h-r)), r, color='#264F92')
                ax.add_artist(circle1)
                ax.add_artist(circle2)
                sub_support(support.pos)
                
        for support in self.supports:
            draw(support)
    
    # dibujar carga puntual    
    def draw_load(self):
        arrow_h = self.L/6.8
        arrow_w = self.L/170
        head_w = self.L/(17/0.35)
        text_dy = arrow_h + arrow_h/4
        if self.load_d == 'down':
            ax.arrow(self.load_pos, arrow_h, 0, -arrow_h, width=arrow_w, head_width=head_w, length_includes_head=True, color='black', linewidth=0.5)
            ax.text(self.load_pos, text_dy, f'{abs(self.load)} kN', horizontalalignment='center', verticalalignment='center', fontsize=8)
            
    # dibujar reacciones
    def draw_reactions(self):
        for support in self.supports:
            arrow_h = self.L/8.5
            arrow_w = self.L/170
            head_w = self.L/(17/0.35)
            text_dy = arrow_h + arrow_h/4
            if support.yreaction > 0:
                ax.arrow(support.pos, -arrow_h, 0, arrow_h, width=arrow_w, head_width=head_w, length_includes_head=True, facecolor='red', linewidth=0.5)
                ax.text(support.pos, -text_dy, f'{support.yreaction} kN', horizontalalignment='center', verticalalignment='center', fontsize=8)
                
    # dibujar solicitado
    def draw(self, solicitado):   # solicitado = ['beam', 'supports', 'load', 'reactions']
        for artist in solicitado:
            if artist == 'beam':
                self.draw_beam()
            elif artist == 'supports':
                self.draw_supports()
            elif artist == 'load':
                self.draw_load()
            elif artist == 'reactions':
                self.draw_reactions()
        plt.show()
    
    # dibujar todo
    def draw_all(self):
        self.draw_beam()
        self.draw_supports()
        self.draw_load()
        self.draw_reactions()
        plt.show()
        
    
v = Beam(10)
v.add_support('pinned', 0)
v.add_support('roller', v.L)
v.add_load(v.L/2, 10, 'down')
v.reactions()

fig, ax = plt.subplots()

# no mostrar ejes
ax.yaxis.set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# plt.tight_layout()
plt.axis('equal')   # 'equal' | 'scaled' | 'tight' | 'auto' | 'image' | 'square'
# plt.grid(linewidth=0.2)   # cuadrícula
# ax.set_axisbelow(True)   # cuadrícula detrás de la gráfica
        
v.draw(['beam', 'supports', 'load', 'reactions'])