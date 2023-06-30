from anastruct import SystemElements
ss = SystemElements(figsize=(10, 4))

ss.add_element(location=[[0, 0], [20, 0]])

ss.add_support_hinged(node_id=1)
ss.add_support_roll(node_id=2)

ss.show_structure()