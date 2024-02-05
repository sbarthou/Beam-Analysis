from beam import Beam


# Inicializa viga, agrega apoyos y cargas
v = Beam(12)
v.add_support('pinned', 0)
v.add_support('roller', v.L)
v.add_distributed_load(3, 6, 6)
v.add_point_load(9, 10)

# Dibuja viga o diagrama
v.draw_moment()