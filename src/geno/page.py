from abc import ABC, abstractmethod
import pathlib
import subprocess

from typing import Any

import panel as pn


class PageBase(ABC):
    @property
    @abstractmethod
    def source_path(self) -> Any:
        raise NotImplementedError

    @property
    @abstractmethod
    def frontmatter(self) -> Any:
        raise NotImplementedError

    @property
    @abstractmethod
    def stylesheets(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def apply_frontmatter(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def render(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def __getitem__(self, key) -> Any:
        return self.frontmatter.get(key, None)

    @abstractmethod
    def __getattr__(self, key) -> Any:
        return self[key]


class MarkdownPage:
    def __init__(
        self,
        markdown: str,
        source_path: pathlib.Path,
        frontmatter: dict[str, Any] | None = None,
        stylesheets: list[str] | None = None,
    ):
        self.markdown = markdown

        self.source_path = source_path
        self.frontmatter = frontmatter or {}
        self.stylesheets = stylesheets or []

        self.apply_frontmatter()

    def apply_frontmatter(self) -> None:
        if self.readtime:
            self.markdown = f"### {self.readtime} Minutes to Read\n\n" + self.markdown

        if self.date:
            self.markdown = f"## {self.date}\n\n" + self.markdown

        self.markdown = f"# {self.title}\n\n" + self.markdown

        # TODO: embed this into a template
        self.markdown += f"\n<script>\n    document.title = '{self.frontmatter['title']} | NESWare.io';</script>"

    def render(self):
        return pn.pane.Markdown(
            self.markdown, max_width=800, stylesheets=self.stylesheets
        )

    def __getitem__(self, key) -> Any:
        return self.frontmatter.get(key, None)

    def __getattr__(self, key):
        return self[key]


class PythonPage:
    def __init__(
        self,
        app: Any,
        source_path: pathlib.Path,
        frontmatter: dict[str, Any] | None = None,
        stylesheets: list[str] | None = None,
    ):
        self.app = app

        self.source_path = source_path
        self.frontmatter = frontmatter or {}
        self.stylesheets = stylesheets or []

        self.apply_frontmatter()

    def apply_frontmatter(self) -> None:
        return

        if self.readtime:
            self.markdown = f"### {self.readtime} Minutes to Read\n\n" + self.markdown

        if self.date:
            self.markdown = f"## {self.date}\n\n" + self.markdown

        self.markdown = f"# {self.title}\n\n" + self.markdown

        # TODO: embed this into a template
        self.markdown += f"\n<script>\n    document.title = '{self.frontmatter['title']} | NESWare.io';</script>"

    def render(self):
        # return pn.pane.Markdown(self.markdown, max_width=800, stylesheets=self.stylesheets)
        subprocess.run(
            f"panel convert {self.app} --to pyodide-worker --out {self.source_path.parent}".split()
        )

    def __getitem__(self, key) -> Any:
        return self.frontmatter.get(key, None)

    def __getattr__(self, key):
        return self[key]
