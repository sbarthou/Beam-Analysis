
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