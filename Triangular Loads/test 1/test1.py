from beam import Beam


# Inicializa viga, agrega apoyos y cargas
v = Beam(10)
v.add_support('pinned', 0)
v.add_support('roller', v.L)
v.add_point_load(5, 10)

# Dibuja viga o diagrama
v.draw_moment()