from Beam import Beam


# Inicializa viga, agrega apoyos y cargas
v = Beam(10)
v.add_support('pinned', 0)
v.add_support('roller', v.L)
v.add_trapezoidal_load(3, 7, 2, 10)

# Dibuja viga o diagrama
v.draw_beam_all()