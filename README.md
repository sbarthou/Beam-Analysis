# Beam Analysis

This is a Python code that allows simple beam analysis, for now, simply supported only.

So far, the 'Distributed Loads' folder contains the 'main.py' file, which is the one that contains the most complete code, i.e. with it you can do all the analysis that this code is capable of.

This is an example of how to use the code:

```python
# Inicializa viga, agrega apoyos y cargas
v = Beam(10)   # Creates an instance of the beam object by providing it with the beam length
v.add_support('pinned', 0)   # Parameters: support_type: "pinned" or "roller", pos: position (int or float)
v.add_support('roller', v.L)   # The L attribute stores the length of the beam.
v.add_point_load(3, 10)   # Parameters: pos: position (int or float), load: load force (int or float)
v.add_distributed_load(5, 7, 5)   # Parameters: start_pos: start position (int or float), end_pos: end position (int or float), load: load force (int or float)

# Dibuja viga o diagrama
v.draw_beam_all()   # Optional parameter: nodes: True (False by default)
```

All drawing methods:

+ `draw_beam_elements(solicitado)`

You can draw different elements to be passed in as a list of strings. The possible elements are `['beam', 'supports', 'loads', 'reactions']`. Optional parameters: `nodes=True` (False by default), `load_lines=True` (False by default).

+ `draw_beam_all()`

Draw all the elements of the beam. Optional parameters: `nodes=True` (False by default), `load_lines=False` (True by default).

+ `draw_shear()`

Draw the shear force diagram. Optional parameter: `nodes=True` (False by default).

+ `draw_moment()`

Draw the bending moment diagram. Optional parameter: `nodes=True` (False by default).
<br>
<br>

**Important:** distributed loads cannot start or end at the beam ends.