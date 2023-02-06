import pygraphviz as pgv

g = pgv.AGraph("input.dot")

for n in g.nodes_iter():
    assert "label" in n.attr.keys()
    l = n.attr["label"]
    print(n.get_name(), l)

for e in g.edges_iter():
    l0 = g.get_node(e[0]).attr["label"]
    l1 = g.get_node(e[1]).attr["label"]
    print(f"{l0} -> {l1}")

