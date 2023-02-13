import typing as tp
import os
import re
import json
import pygraphviz as pgv
from pathlib import Path

# Example string: '<b>Definition:</b> audio_datapath.c:763</div>'
DEFINITION_REGEX = re.compile(r'<b>Definition:</b> (\w+\.\w+):(\d+)</div>')

class NodeTranslator:
    def __init__(self, input_dot_file: Path):
        self.g = pgv.AGraph(input_dot_file)
        self.in_stem = input_dot_file.stem
        self.in_parent = input_dot_file.resolve().parent

        self._derive_out_stem()
        self._parse_nodes_for_summary()

    def _derive_out_stem(self):
        tokens = self.in_stem.split('_')
        assert tokens[-1].endswith('cgraph'), f"Expected {self.in_stem}.dot stem to end in cgraph"
        assert tokens[-3] in ['8h', '8c'], f"Expected '_8h_' or '_8c_' before the hash in {self.in_stem}.dot stem"
        tokens[-2] = self.g.get_name()

        self.out_stem = "_".join(tokens)

    def _parse_nodes_for_summary(self):
        self.nodes = {
            "original_filename": self.in_stem + ".dot"
        }
        for n in self.g.nodes_iter():
            assert "label" in n.attr.keys()
            d = {
                "label": n.attr["label"].replace('\\l', '')
            }

            if "URL" in n.attr.keys():
                src_file, line_num = self._derive_source_from_URL(n.attr["URL"], d["label"])
            else:
                src_file, line_num = self._derive_source_from_in_stem(d["label"])

            if src_file is None:
                src_file, line_num = self._scan_all_html_sources_for_src_file(d["label"])

                if src_file is None:
                    src_file = "UNKNOWN.c"
                    line_num = -1
                else:
                    src_file = src_file + " MAYBE "

            d["src_file"] = src_file
            d["src_line"] = line_num
            d["dflw_name"] = src_file.replace(' MAYBE ', '').replace('.', '_8') + "__" + d["label"]

            self.nodes[n.get_name()] = d

    def _derive_source_from_in_stem(self, method_name: str) -> tp.Tuple[str, int]:
        tokens = self.in_stem.split('_')
        tokens[-3] = "8h_source.html"

        src_html_file = '_'.join(tokens[:-2])

        return self._parse_src_html_for_line_num(self.in_parent / src_html_file, method_name)

    def _derive_source_from_URL(self, url: str, method_name: str) -> tp.Tuple[str, int]:
        assert ".html" in url, f"Expected {method_name} to have a URL with '.html' in it, got {url}"
        url_stem = url.split('.html')[0]
        if url_stem.startswith('$'):
            url_stem = url_stem[1:]

        assert url_stem[-2:] in ('8c', '8h'), f"Expected {method_name} to have a URL stem ending in either '8c' or '8h', got {url}"

        src_html_file = url_stem[:-2] + '8h_source.html'

        return self._parse_src_html_for_line_num(self.in_parent / src_html_file, method_name)

    def _parse_src_html_for_line_num(self, src_html_file: Path, method_name: str) -> tp.Tuple[str, int]:
        method_name = f" {method_name}("

        if not os.path.exists(src_html_file):
            return None, None

        with open(src_html_file, "r") as inF:
            for line in inF:
                if method_name in line:
                    m = DEFINITION_REGEX.search(line)
                    if m:
                        # .c file name and line number
                        return m.group(1), int(m.group(2))

        return None, None

    def _scan_all_html_sources_for_src_file(self, method_name: str) -> tp.Tuple[str, int]:
        all_src_files = self.in_parent / "*source.html"
        for filename in self.in_parent.glob("*source.html"):
            src_file, line_num = self._parse_src_html_for_line_num(filename, method_name)
            if src_file is not None:
                return src_file, line_num

        return None, None

    def write_node_summary(self, outdir: Path):
        outpath = outdir / f"{self.out_stem}.nsumm"
        with open(outpath, "w") as outF:
            json.dump(self.nodes, outF, indent=4)
        print(f"Wrote {outpath}")

    def read_node_summary(self, in_nsumm_file: Path):
        with open(in_nsumm_file, "r") as inF:
            self.nodes = json.load(inF)


