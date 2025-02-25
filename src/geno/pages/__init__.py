import functools

import panel as pn

from .markdown import MarkdownPage
from .python import PythonPage
from .pyodide import PyodidePage


class RenderTemplate:
    def __init__(self, configuration, header=None, sidebar=None, modal=None):
        self.template = functools.partial(
            pn.template.BootstrapTemplate,
            title=configuration["title"],
            header_color=configuration["header_color"],
            header_background=configuration["header_background"],
            logo=configuration["logo"],
            favicon="/favicon.ico",
            header=header or [],
            sidebar=sidebar or [],
            modal=modal or [],
        )

    def render(self, page, site, stylesheets, **kwargs):
        page.dst.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(page, MarkdownPage):
            tmp = self.template(main=page.render(site, stylesheets), **kwargs)
            tmp.save(page.dst)
        else:
            page.render(site, stylesheets)
