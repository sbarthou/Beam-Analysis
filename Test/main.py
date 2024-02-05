from Beam import Beam


# Inicializa viga, agrega apoyos y cargas
v = Beam(10)
v.add_support('pinned', 0)
v.add_support('roller', v.L)
# v.add_point_load(5, 5)
# v.add_distributed_load(5, v.L, 5)
# v.add_triangular_load(5, v.L, 5, 'ascending')

# Dibuja viga o diagrama
v.draw_shear()
