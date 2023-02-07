import os
import argparse
from pathlib import Path
from lib.node_translator import NodeTranslator

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

