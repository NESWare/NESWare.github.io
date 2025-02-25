import pathlib
from typing import Any

import panel as pn
import yaml
from jinja2 import Environment, FileSystemLoader


environment = Environment(loader=FileSystemLoader("templates/"))


class MarkdownPage:
    def __init__(
        self,
        src: pathlib.Path,
        dst: pathlib.Path,
    ):
        self.src = src
        self.dst = dst
        self.link = dst.relative_to(dst.parts[0])

        with open(src) as s:
            self.markdown = s.read()
            self.frontmatter = {}

        if "---fm---" in self.markdown:
            frontmatter, self.markdown = self.markdown.split("---fm---", 1)
            self.frontmatter = yaml.safe_load(frontmatter)

    def render(
        self,
        site,
        stylesheets,
    ):
        template = environment.get_template(self.frontmatter.get("layout", "default"))
        markdown = template.render(
            content=self.markdown, page=self.frontmatter, site=site
        )

        template = environment.from_string(markdown)
        markdown = template.render(
            content=self.markdown, page=self.frontmatter, site=site
        )

        return pn.pane.Markdown(
            markdown,
            max_width=800,
            sizing_mode="stretch_width",
            align="center",
            stylesheets=stylesheets,
        )

    def __getitem__(self, key) -> Any:
        return self.frontmatter.get(key, None)

    def __getattr__(self, key):
        return self[key]
