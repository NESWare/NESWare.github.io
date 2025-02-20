import datetime

import panel as pn


stylesheets = <<<css>>>


frontmatter = {
    "title": "Panel & Pyodide & WASM, Oh My!",
    "section": "blog",
    "date": datetime.datetime.strptime("2025-02-19", "%Y-%m-%d").date(),
    "tags": "c++ python dashboarding visualization panel holoviews pybind11".split(),
    "readtime": 10,
}


def app():
    main = pn.Column()

    main.append(
        pn.pane.Markdown(
            """# Now
            Now that I am using `panel` as the core of this blog, the doors are blown pretty wide open as far as what can be done. I can't possibly cover everything that `panel` does, but take a peek at the [App Gallery](https://panel.holoviz.org/gallery/index.html) to get an idea. It is pretty incredible how easy `panel` makes everything, which is why I was mildly shocked I never thought about doing this sooner.""",
            max_width=800,
            stylesheets=stylesheets,
        )
    )

    main.append(
        pn.pane.Markdown(
            """There are a ton of new opportunities to not only use `panel` to render the markdown (as `geno` was initially written to do), but we can also render `panel` apps using `pyodide`. This means that interactive applications can be written to run in the browser, instead of serving static HTML/CSS/JS. This gets even crazier if that interactive application in the browser is also utilizing "native" code targeted at WASM! Ultimately I want to write a `panel` app that I can convert to a `pyodide` application, and I want that application to run a C++ library in real-time so that I can visualize the model and some analysis. All in the browser.""",
            max_width=800,
            stylesheets=stylesheets,
        )
    )

    main.append(
        pn.pane.Markdown(
            """Let's not get ahead of ourselves though... first, we need a way of telling `geno` to simply pull in `panel` applications and get them rendered statically, since all we can do now is render markdown.
            """,
            max_width=800,
            stylesheets=stylesheets,
        )
    )

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

    pn.template.BootstrapTemplate.config.raw_css.extend(stylesheets)

    return pn.template.BootstrapTemplate(
        title="NESWare",
        header_color="#FFFFFF",
        header_background="#009926",
        logo="assets/images/nesware/nesware-logo-textless-white.png",
        favicon="/favicon.ico",
        main=main,
        sidebar=pn.Column(*buttons),
        sidebar_width=240,
    )

app().servable()
