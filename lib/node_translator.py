import json
import pygraphviz as pgv
from pathlib import Path

class NodeTranslator:
    def __init__(self, input_dot_file: Path):
        self.g = pgv.AGraph(input_dot_file)
        self.in_stem = input_dot_file.stem
        self.in_parent = input_dot_file.resolve().parent

        self._parse_nodes_for_summary()

    def _parse_nodes_for_summary(self):
        self.nodes = {}
        for n in self.g.nodes_iter():
            assert "label" in n.attr.keys()
            d = {
                "label": n.attr["label"]
            }

            if "url" in n.attr.keys():
                d["url"] = n.attr["url"]

            self.nodes[n.get_name()] = d

    def write_node_summary(self, outdir: Path):
        outpath = outdir / f"{self.in_stem}.nsumm"
        with open(outpath, "w") as outF:
            json.dump(self.nodes, outF, indent=4)

    def read_node_summary(self, in_nsumm_file: Path):
        with open(in_nsumm_file, "r") as inF:
            self.nodes = json.load(inF)



def test_edge_iter():
    """Unused example"""
    for e in g.edges_iter():
        l0 = g.get_node(e[0]).attr["label"]
        l1 = g.get_node(e[1]).attr["label"]
        print(f"{l0} -> {l1}")

