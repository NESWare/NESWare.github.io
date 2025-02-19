import pathlib
import shutil

import panel as pn
import yaml

from .css import CSS
from .page import Page


def main():
    static = pathlib.Path("static")
    if static.exists():
        shutil.rmtree(
            static,
        )
    static.mkdir()

    shutil.copytree("./assets", static / "assets")
    shutil.copy("assets/images/nesware/nesware-logo-textless-64px.ico", static / "favicon.ico")
    with open(static / ".htaccess", "w") as htaccess:
        htaccess.write("DirectoryIndex index.html")

    pathlib.Path(static / ".nojekyll").touch()

    css = CSS(pathlib.Path("assets") / "css")

    content = pathlib.Path("content")

    def split_frontmatter_from_content(md_content: str) -> tuple[str, str]:
        if "---fm---" in md_content:
            frontmatter, content = md_content.split("---fm---", 1)
            return (frontmatter, content)
        return ("", md_content)

    def md_to_html(md_path: pathlib.Path) -> Page:
        new_path = static / (md_path.relative_to(content))
        with open(md_path) as md_file:
            new_path.parent.mkdir(exist_ok=True, parents=True)
            fm, md = split_frontmatter_from_content(md_file.read())
            return Page(
                new_path.with_suffix(".html"), md, yaml.safe_load(fm), css.stylesheets
            )

    main_pages = [
        md_to_html(content / "index.md"),
        md_to_html(content / "blog.md"),
        md_to_html(content / "projects.md"),
        md_to_html(content / "about.md"),
    ]
    blog_pages = [md_to_html(md) for md in (content / "blog").glob("*.md")]
    project_pages = [md_to_html(md) for md in (content / "projects").glob("*.md")]

    blog_pages.sort(key=lambda p: p.date)

    for page in reversed(blog_pages):
        main_pages[
            0
        ].md += f"\n\n### [{page.date} {page.title}]({page.source_path.relative_to(static)})"
        break

    for page in reversed(blog_pages):
        main_pages[
            1
        ].md += f"\n\n### [{page.date} {page.title}]({page.source_path.relative_to(static)})"

    pages = main_pages + blog_pages + project_pages

    button_config = {
        "button_type": "success",
        "button_style": "outline",
        "sizing_mode": "stretch_width",
        "stylesheets": [":hover { background-color: #e8fff4; }"],
    }

    buttons = []
    for page_name in ["Home", "Blog", "Projects", "About"]:
        button = pn.widgets.Button(name=page_name, **button_config)
        button.js_on_click(
            code=f'window.location = "/{"" if page_name == "Home" else page_name.lower() + ".html"}"'
        )
        buttons.append(button)

    pn.template.BootstrapTemplate.config.raw_css.extend(css.stylesheets)

    for page in pages:
        main = pn.Column(
            page.markdown,
            sizing_mode="stretch_width",
            align="center",
        )

        pn.template.BootstrapTemplate(
            title="NESWare",
            header_color="#FFFFFF",
            header_background="#009926",
            logo="assets/images/nesware/nesware-logo-textless-white.png",
            main=main,
            sidebar=pn.Column(*buttons),
            sidebar_width=240,
        ).save(page.source_path)
