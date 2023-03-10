"""
Get *cgraph.dot and *icgraph.dot input files by doing this:

doxygen -g hmm.doxy

EXTRACT_ALL     = YES
EXTRACT_PRIVATE = YES
RECURSIVE       = YES
HAVE_DOT        = YES
DOT_CLEANUP     = NO
CALL_GRAPH      = YES
CALLER_GRAPH    = YES

doxygen hmm.doxy
"""

import os
import argparse
from pathlib import Path
from lib.node_translator import NodeTranslator
from lib.dot_flow_exporter import DotFlowExporter

def setup_arg_parse():
    desc="some description"

    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('input_file', type=Path, help="path to .dot file to translate")
    parser.add_argument('--outdir', type=Path, default=Path('./node_out'), help=\
        "path to output dir, output filename will be based on the input filename")

    return parser

if __name__ == '__main__':
    args = setup_arg_parse().parse_args()
    assert os.path.exists(args.outdir), f"Create output folder '{args.outdir}' first"

    t = NodeTranslator(args.input_file)
    t.write_node_summary(args.outdir)

    e = DotFlowExporter(args.input_file, t)
    e.write_dflow_file(args.outdir)

