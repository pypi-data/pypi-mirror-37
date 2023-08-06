import os

import pkg_resources

from htmlc.elements.link import Link
from htmlc.utils import file_dir

ALWAYS_INCLUDE = [
    "boolean.h"
]


class CLinker:

    def __init__(self, element_tree, doctype):
        self.htmlc_includes = {*ALWAYS_INCLUDE}
        self.includes = set()
        self.element_tree = element_tree
        self.doctype = doctype
        self.__find_includes(element_tree)

    def __find_includes(self, elements):
        for el in elements:
            self.htmlc_includes.update(el.require_htmlc_includes)
            self.includes.update(el.require_includes)
            self.__find_includes(el.children)

    def get_includes_code(self):
        c = ""
        for hi in self.htmlc_includes:
            c += f'#include "htmlc/{hi}"\n'
        c += "\n"
        for i in self.includes:
            c += f"#include <{i}>\n"
        return c

    def save_htmlc_files(self, out_dir):
        out_dir += "htmlc/"
        for hi in self.htmlc_includes:
            hi_file = out_dir + hi
            hi_dir = file_dir(hi_file)
            if not os.path.exists(hi_dir):
                os.makedirs(hi_dir)
            with open(hi_file, "w") as f:
                f.write(
                    pkg_resources.resource_string(__name__, "data/c_code/" + hi)
                        .decode('utf-8')
                        .replace("\r", "")
                )
                f.close()
