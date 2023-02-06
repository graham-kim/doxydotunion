import pygraphviz as pgv

g = pgv.AGraph(strict=True, directed=True)

g.add_node("Node1", label="abc")
g.add_node("Node2", label="def")
g.add_edge("Node1", "Node2")

g.write("hmm.dot")

