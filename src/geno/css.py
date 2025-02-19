import pathlib


class CSS:
    def __init__(self, css_path: pathlib.Path) -> None:
        self.stylesheets = [open(css).read() for css in css_path.glob("*.css")]
