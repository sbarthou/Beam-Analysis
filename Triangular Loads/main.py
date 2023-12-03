from BeamAscending import Beam


# Inicializa viga, agrega apoyos y cargas
v = Beam(15)
v.add_support("pinned", 0)
v.add_support("roller", v.L)
v.add_distributed_load(1, 4, 1)
v.add_triangular_load(6, 9, 2, "ascending")
v.add_point_load(13, 3)

# Dibuja viga o diagrama
# v.draw_beam_all()
v.draw_moment(max_value=True)
