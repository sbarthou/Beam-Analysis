from Beam import Beam


# Inicializa viga, agrega apoyos y cargas
v = Beam(15)
v.add_support('pinned', 0)
v.add_support('roller', v.L)
v.add_triangular_load(1, 4, 5, 'descending')
v.add_distributed_load(5, 7, 4)
v.add_point_load(9, 15)
v.add_trapezoidal_load(11, 14, 1, 5)

# Dibuja viga o diagrama
v.draw_shear()