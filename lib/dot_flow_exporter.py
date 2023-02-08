import typing as tp
import pygraphviz as pgv
from pathlib import Path
from lib.node_translator import NodeTranslator

class DotFlowExporter:
    def __init__(self, input_dot_file: Path, node_t: NodeTranslator):
        self.g = pgv.AGraph(input_dot_file)
        self.in_stem = input_dot_file.stem
        self.in_parent = input_dot_file.resolve().parent
        self.node_lookup: tp.Dict[str, tp.Dict[str, tp.Any]] = node_t.nodes

    def write_dflow_file(self, outdir: Path):
        outpath = outdir / f"{self.in_stem}.dflw"
        with open(outpath, "w") as outF:
            for v in self.node_lookup.values():
                outF.write( \
f'- {v["dflw_name"]} | {v["label"]}()\\n\\n{v["src_file"]}\\n{v["src_line"]}\n\n' \
                )

            for e in self.g.edges_iter():
                n0 = self.node_lookup[ self.g.get_node(e[0]).get_name() ]
                n1 = self.node_lookup[ self.g.get_node(e[1]).get_name() ]

                outF.write( \
f'< {n0["dflw_name"]}\n' \
                )
                outF.write( \
f'> {n1["dflw_name"]}\n\n' \
                )

