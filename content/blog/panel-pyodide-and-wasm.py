import datetime

import holoviews as hv
import numpy as np
import pandas as pd
import panel as pn
import pygments


pn.extension()

stylesheets = []


frontmatter = {
    "title": "Panel & Pyodide & WASM, Oh My!",
    "section": "blog",
    "date": datetime.datetime.strptime("2025-02-19", "%Y-%m-%d").date(),
    "tags": "c++ python dashboarding visualization panel holoviews pybind11".split(),
    "readtime": 10,
}


callback = None


def markdown(txt):
    return pn.pane.Markdown(
        txt,
        max_width=800,
        stylesheets=stylesheets,
    )


def cannonball_simulation():
    class Cannonball:
        def __init__(self, x, y, vx, vy):
            self.x = x
            self.y = y
            self.vx = vx
            self.vy = vy

        def update(self, dt):
            self.x += self.vx * dt
            self.y += self.vy * dt
            self.vy += -9.81 * dt

    cb = Cannonball(0.0, 0.0, 0.0, 0.0)

    launch_angle_slider = pn.widgets.FloatSlider(
        name="Launch Angle (degrees)", start=0, end=90, value=45, step=1
    )
    launch_speed_slider = pn.widgets.FloatSlider(
        name="Launch Speed (units/second)", start=0, end=20, value=10, step=1
    )
    launch_button = pn.widgets.Button(name="Launch!")

    stream = hv.streams.Pipe(data=[])

    def cannonball():
        cb.update(0.1)
        stream.send(pd.DataFrame({"x": [cb.x], "y": [cb.y]}))
        if cb.y <= 0.0:
            callback.stop()

    def launch(event):
        global callback
        if callback is not None:
            callback.stop()
            callback = None

        cb.x = 0.0
        cb.y = 0.0
        cb.vx = launch_speed_slider.value * np.cos(
            np.deg2rad(launch_angle_slider.value)
        )
        cb.vy = launch_speed_slider.value * np.sin(
            np.deg2rad(launch_angle_slider.value)
        )
        callback = pn.state.add_periodic_callback(cannonball, 33, timeout=5000)

    launch_button.on_click(launch)

    def view(data):
        return hv.Points(data, kdims=["x", "y"])

    dmap = hv.DynamicMap(view, streams=[stream]).opts(
        xlim=(0.0, 50.0), ylim=(0.0, 30.0), width=600, height=480, shared_axes=False
    )

    return pn.Row(
        dmap, pn.Column(launch_angle_slider, launch_speed_slider, launch_button)
    )


def sandpile_simulation():
    class Sandpile:
        def __init__(self, n):
            self.n = n
            self.sandpile = np.zeros((n, n), dtype=np.int32) + 4

        def reset(self):
            self.sandpile = np.zeros_like(self.sandpile, dtype=np.int32) + 4

        def perturb(self):
            self.sandpile[*np.random.random_integers(0, self.n - 1, size=2)] += 1
            self.collapse()

        def viz_perturb(self, stream):
            # self.sandpile[*np.random.random_integers(0, self.n - 1, size=2)] += 1
            self.viz_collapse(stream)

        def collapse(self):
            while np.any((mask := self.sandpile >= 4)):
                rows, cols = np.where(mask)
                for r, c in zip(rows, cols):
                    self.sandpile[r, c] -= 4
                    if r < (self.n - 1):
                        self.sandpile[r + 1, c] + 1
                    if r > 0:
                        self.sandpile[r - 1, c] + 1
                    if c < (self.n - 1):
                        self.sandpile[r, c + 1] + 1
                    if c > 0:
                        self.sandpile[r, c - 1] + 1

        def viz_collapse(self, stream):
            if np.any((mask := self.sandpile >= 4)):
                rows, cols = np.where(mask)
                for r, c in zip(rows, cols):
                    self.sandpile[r, c] -= 4
                    if r < (self.n - 1):
                        self.sandpile[r + 1, c] += 1
                    if r > 0:
                        self.sandpile[r - 1, c] += 1
                    if c < (self.n - 1):
                        self.sandpile[r, c + 1] += 1
                    if c > 0:
                        self.sandpile[r, c - 1] += 1
                    if not callback.running:
                        break

                stream.send(self.sandpile)

    asp = Sandpile(10)

    launch_button = pn.widgets.Button(name="Launch!")
    reset_button = pn.widgets.Button(name="Reset")

    stream = hv.streams.Pipe(data=[])

    def sandpile():
        asp.viz_perturb(stream)

    def launch(event):
        global callback
        if callback is not None and callback.running:
            callback.stop()
            callback.running = False
            launch_button.name = "Launch!"
        elif callback is not None and not callback.running:
            callback.start()
            launch_button.name = "Stop!"
        else:
            asp.reset()
            callback = pn.state.add_periodic_callback(sandpile, 33)
            launch_button.name = "Stop!"

    def reset(event):
        global callback
        if callback is not None:
            callback.stop()
        callback = None
        asp.reset()
        stream.send(asp.sandpile)
        launch_button.name = "Launch!"

    launch_button.on_click(launch)
    reset_button.on_click(reset)

    def view2(data):
        return hv.Image(data)

    dmap2 = hv.DynamicMap(view2, streams=[stream]).opts(
        xlim=(-0.5, 0.5),
        ylim=(-0.5, 0.5),
        clim=(0, 4),
        xaxis="bare",
        yaxis="bare",
        width=600,
        height=480,
        shared_axes=False,
        show_grid=True,
    )

    return pn.Row(dmap2, pn.Column(launch_button, reset_button))


main = pn.Column()

main.append(
    pn.pane.Markdown(
        "# HEY, LISTEN! There is some cool stuff loading, be a little patient!",
        max_width=800,
    )
)

main.append(
    markdown(
        """## Blast Off!

Now that I am using `panel` as the core of this blog, the doors are blown pretty wide open as far as what can be done (well, this _could_ all be done before, but now _I_ can do it!). I can't possibly cover everything that `panel` does, but take a peek at the [App Gallery](https://panel.holoviz.org/gallery/index.html) to get an idea. It is pretty incredible how easy `panel` makes everything, which is why I was mildly shocked I never thought about doing this sooner.

There are a ton of new opportunities to not only use `panel` to render the markdown (as `geno` was initially written to do), but we can also render `panel` apps using `pyodide`. This means that interactive applications can be written to run in the browser, instead of serving plain HTML/CSS/JS. This gets even crazier if that interactive application in the browser is also utilizing "native" code targeted at WASM. Ultimately I want to write a `panel` app that I can convert to a `pyodide` application, and I want that application to run a C++ library in real-time so that I can visualize the model and some analysis. **All in the browser**.

Let's not get ahead of ourselves though... first, we need a way of telling `geno` to simply pull in `panel` applications and get them rendered statically, since all we can do now is render markdown. For a simple `panel` app this is actually quite easy since we are technically doing this already for the markdown pages:

```python
pn.template.BootstrapTemplate(
    # ...
    main=main,
    # ...
).save(page.source_path)
```

We use this call in `geno` with the markdown inserted into the `main` component of the final layout. We can have regular "apps" do the same thing. This is pretty trivial. The thing is, this is giving us more static sites. We cut ourselves off from really benefitting from what `panel` can do! We want to be able to actually run the `panel` application as a post - enter [`pyodide`](https://pyodide.org/en/stable/). This stuff is absolutely voodoo to me - all I know is that `pyodide` is a distribution of Python that targets `WebAssembly` instead of your native system. [`WebAssembly`](https://en.wikipedia.org/wiki/WebAssembly) is also voodoo to me, but I like to think of it as a high-performance runtime that is compatible with your web browser (for better or worse, correct or incorrect, this is how I think of it).

So what does this all mean? This means we can write `panel` applications in Python, and then actually run them in our browser using `pyodide`. This deeply contrasts running Python locally on some machine. You may have noticed some odd loading overlay when you first navigated here - well, this page is actually a `panel` application running with `pyodide` within your browser! This means we can do some pretty nifty things - maybe we can implement a cannon-ball simulation, configure it, and be able to run and visualize it all right here:
"""
    )
)

main.append(cannonball_simulation())

main.append(
    markdown(
        """Pretty neat, right? I think so. That model was coded in Python and hooked into `panel` and `holoviews`, **and it is running in your browser**. There are some challenges I am still working through though, largely because I am extremely new to `pyodide` and how it all works with `panel`. Namely, your `pyodide` application cannot embed/use local modules/packages; it must be able to install them (effectively) through [PyPI](https://pypi.org/). This means that your entire application needs to be self-contained. This is less of a roadblock and just some new terrain to map out.
             
I have some janky ways of injecting the custom CSS and getting the same consistent layout working. It works great, but is _janky and bad_ and I will be looking at different ways of injecting those bits.
""",
    )
)

main.append(sandpile_simulation())

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

pn.template.BootstrapTemplate(
    title="NESWare",
    header_color="#FFFFFF",
    header_background="#009926",
    logo="assets/images/nesware/nesware-logo-textless-white.png",
    favicon="/favicon.ico",
    main=main,
    sidebar=pn.Column(*buttons),
    sidebar_width=240,
).servable()
