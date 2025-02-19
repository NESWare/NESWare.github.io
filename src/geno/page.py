import pathlib
from typing import Any

import panel as pn


class Page:
    def __init__(
        self,
        source_path: pathlib.Path,
        md: str,
        fm: dict[str, Any] | None = None,
        ss: list[str] | None = None,
    ):
        self.source_path = source_path

        self.md = md
        self.fm = fm or {}
        self.ss = ss or []

        self.update_md_with_fm()

    def update_md_with_fm(self) -> None:
        if self.readtime:
            self.md = f"### {self.readtime} Minutes to Read\n\n" + self.md

        if self.date:
            self.md = f"## {self.date}\n\n" + self.md

        self.md = f"# {self.title}\n\n" + self.md

        # TODO: embed this into a template
        self.md += f"\n<script>\n    document.title = '{self.fm['title']} | NESWare.io';</script>"

    def __getitem__(self, key) -> Any:
        return self.fm.get(key, None)

    def __getattr__(self, key):
        return self[key]

    @property
    def markdown(self):
        return pn.pane.Markdown(self.md, max_width=800, stylesheets=self.ss)
