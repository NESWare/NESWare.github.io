import argparse
import pathlib
import shutil

import panel as pn
import yaml

from .css import CSS
from .pages import MarkdownPage, PyodidePage, RenderTemplate


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "configuration", type=pathlib.Path, help="geno configuration file"
    )
    inputs = parser.parse_args()

    with open(inputs.configuration) as cf:
        configuration = yaml.safe_load(cf)

    static = pathlib.Path("static")
    if static.exists():
        shutil.rmtree(
            static,
        )
    static.mkdir()

    shutil.copytree("./assets", static / "assets")
    shutil.copy(configuration["favicon"], static / "favicon.ico")

    with open(static / ".htaccess", "w") as htaccess:
        htaccess.write("DirectoryIndex index.html")

    css = CSS(pathlib.Path("assets") / "css")

    content = pathlib.Path("content")

    site = {"pages": {"all": []}, "title": configuration["title"]}

    # TODO: Update to read "nav" from configuratino
    for page in content.glob("**/*"):
        if "__pycache__" in page.parts:
            continue

        dst = (static / (page.relative_to(content))).with_suffix(".html")

        match page.suffix:
            case ".md":
                site["pages"]["all"].append(MarkdownPage(page, dst))
            # case ".py":
            #     site["pages"]["all"].append(PythonPage(page, dst))
            case ".py":
                site["pages"]["all"].append(PyodidePage(page, dst))
            case _:
                continue

        p = site["pages"]["all"][-1].dst.relative_to(static)
        if p.name == "index.html":
            main_pages = site["pages"].setdefault("main", [])
            main_pages.append(site["pages"]["all"][-1])

        if "blog" in p.parts and p.stem != "index":
            blog_pages = site["pages"].setdefault("blog", [])
            blog_pages.append(site["pages"]["all"][-1])

        if "projects" in p.parts and p.stem != "index":
            project_pages = site["pages"].setdefault("projects", [])
            project_pages.append(site["pages"]["all"][-1])

    blog_pages.sort(key=lambda p: p.date, reverse=True)

    buttons = []
    # TODO: Update to read "nav" from configuratino
    for page_name, page_file in configuration["navigation"]["main"].items():
        button = pn.widgets.Button(name=page_name, **configuration["button"])
        button.js_on_click(
            code=f'window.location = "/{"" if page_name == "Home" else page_name.lower() + ".html"}"'
        )
        buttons.append(button)

    pn.template.BootstrapTemplate.config.raw_css.extend(css.stylesheets)

    rt = RenderTemplate(
        configuration,
        header=pn.Row(pn.Spacer(width=configuration["button"]["width"]), *buttons),
    )
    for page in site["pages"]["all"]:
        rt.render(
            page,
            site,
            css.stylesheets,
            sidebar_width=240,
        )
