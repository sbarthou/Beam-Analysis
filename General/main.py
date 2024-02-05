from Beam import Beam


# Inicializa viga, agrega apoyos y cargas
v = Beam(10)
v.add_support('pinned', 0)
v.add_support('roller', 5)
v.add_point_load(8, 10)

# Dibuja viga o diagrama
v.draw_moment(max_value=True)
