from Beam import Beam


# Inicializa viga, agrega apoyos y cargas
v = Beam(10)
v.add_support("pinned", 0)
v.add_support("roller", v.L)
v.add_triangular_load(1, 9, 10, 'ascending')

# Dibuja viga o diagrama
v.draw_shear()
