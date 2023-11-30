from Beam1 import Beam


# Inicializa viga, agrega apoyos y cargas
v = Beam(20)
v.add_support('pinned', 0)
v.add_support('roller', v.L)
v.add_distributed_load(2, 4, 3)
v.add_point_load(7, 10)
v.add_simple_triangular_load(10, 14, 5, 'ascending')
v.add_simple_triangular_load(16, 19, 5, 'descending')

# Dibuja viga o diagrama
v.draw_beam_all()