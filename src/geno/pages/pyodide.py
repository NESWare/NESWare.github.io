import importlib.util
import pathlib
import shutil
import subprocess
import sys
from typing import Any

import yaml
from jinja2 import Environment, FileSystemLoader

environment = Environment(loader=FileSystemLoader("templates/"))


def load_module_from_path(module_path):
    spec = importlib.util.spec_from_file_location(module_path.stem, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    sys.modules[module_path.stem] = module
    return module


class PyodidePage:
    def __init__(
        self,
        src: pathlib.Path,
        dst: pathlib.Path,
    ):
        self.src = src
        self.dst = dst
        self.link = dst.relative_to(dst.parts[0])

        with open(src) as s:
            self.app = s.read()
            self.frontmatter = {}

        if "---fm---" in self.app:
            frontmatter, self.app = self.app.split("---fm---", 1)
            self.frontmatter = yaml.safe_load(frontmatter)

    def render(self, site, stylesheets):
        template = environment.from_string(self.app)
        app = template.render(
            content=self.markdown, page=self.frontmatter, site=site, css=stylesheets
        )
        with open(self.dst.with_suffix(".py"), "w") as t:
            t.write(app)

        subprocess.run(
            f"panel convert {self.dst.with_suffix('.py')} --to pyodide-worker --out {self.dst.parent}".split()
        )

    def __getitem__(self, key) -> Any:
        return self.frontmatter.get(key, None)

    def __getattr__(self, key):
        return self[key]
