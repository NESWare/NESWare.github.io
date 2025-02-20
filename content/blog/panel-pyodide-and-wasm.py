# A proof-of-concept (that requires a ton of documentation and comments!)
#

import datetime

import holoviews as hv
import numpy as np
import pandas as pd
import panel as pn
import pygments

pn.extension()

# frontmatter, implemented directly as a dict
frontmatter = {
    "title": "Panel & Pyodide & WASM, Oh My!",
    "section": "blog",
    "date": datetime.datetime.strptime("2025-02-19", "%Y-%m-%d").date(),
    "tags": "c++ python dashboarding visualization panel holoviews pybind11".split(),
    "readtime": 10,
}

# stylesheets; janky but we replace this string (the invalid Python) with the actual CSS overrides
stylesheets = <<<css>>>

# define global callbacks up here, one for each "system" we want to run 
cannonball_callback = None
sandpile_callback = None

def markdown(txt: str) -> pn.pane.Markdown:
    """Simple utility to produce the markdown pane with the same style"""
    return pn.pane.Markdown(
        txt,
        max_width=800,
        stylesheets=stylesheets,
    )

def cannonball_simulation() -> None:
    """Produces a self-contained sub-application for us to embed. This application is a simple cannon-ball simulation that lets users select a launch angle and launch speed for the cannon-ball and then launch it.
    """
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

    # create widgets
    launch_angle_slider = pn.widgets.FloatSlider(
        name="Launch Angle (degrees)", start=0, end=90, value=45, step=1
    )
    launch_speed_slider = pn.widgets.FloatSlider(
        name="Launch Speed (units/second)", start=0, end=20, value=10, step=1
    )
    launch_button = pn.widgets.Button(name="Launch!")

    # create an instance of the Cannonball class to use for the simulation
    cannonball = Cannonball(0.0, 0.0, 0.0, 0.0)

    # function to schedule periodically; this will be called repeatedly until the simulation is over
    # it will update the cannon-ball, stream the data, and then stop the callback (if the simulation is over).
    def update_cannonball():
        cannonball.update(0.1)
        stream.send(pd.DataFrame({"x": [cannonball.x], "y": [cannonball.y]}))
        if cannonball.y <= 0.0:
            cannonball_callback.stop()

    # function to tie to the launch button; this resets the cannon-ball and schedules the simulation
    def launch(event):
        global cannonball_callback
        if cannonball_callback is not None:
            cannonball_callback.stop()
            cannonball_callback = None

        cannonball.x = 0.0
        cannonball.y = 0.0
        cannonball.vx = launch_speed_slider.value * np.cos(
            np.deg2rad(launch_angle_slider.value)
        )
        cannonball.vy = launch_speed_slider.value * np.sin(
            np.deg2rad(launch_angle_slider.value)
        )
        cannonball_callback = pn.state.add_periodic_callback(update_cannonball, 50)

    # tie the launch function to the launch button
    launch_button.on_click(launch)

    # callback to execute whenever we stream data
    def view(data):
        return hv.Points(data, kdims=["x", "y"])

    # create a data stream for to animate our model data
    stream = hv.streams.Pipe(data=[])

    # dynamic map that listens to the stream
    dmap = hv.DynamicMap(view, streams=[stream]).opts(
        xlim=(0.0, 50.0),
        ylim=(0.0, 30.0),
        width=600,
        height=480,
        shared_axes=False,
        show_grid=True,
    )

    # pack everything together!
    return pn.Row(
        dmap, pn.Column(launch_angle_slider, launch_speed_slider, launch_button)
    )


def sandpile_simulation():
    """Produces a self-contained sub-application for us to embed. This application is a simple implementation of the Abelian Sandpile Model. Select the size of the sandpile and launch it!
    """
    class Sandpile:
        def __init__(self, n):
            self.n = n
            self.sandpile = np.zeros((n, n), dtype=np.int32) + 4

        def reset(self, n):
            self.n = n
            self.sandpile = np.zeros((n, n), dtype=np.int32) + 4

        def perturb(self):
            self.sandpile[*np.random.random_integers(0, self.n - 1, size=2)] += 1

        def stabilize(self):
            while np.any((mask := self.sandpile >= 4)):
                self.collapse(mask)

        def collapse(self, mask=None):
            mask = mask if mask else (self.sandpile >= 4)
            if np.any(mask):
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

        @property
        def stable(self):
            return np.all(self.sandpile < 4)

    # create widgets
    launch_button = pn.widgets.Button(name="Launch!")
    reset_button = pn.widgets.Button(name="Reset")
    dimension_slider = pn.widgets.IntSlider(
        name="Launch Angle (degrees)", start=1, end=50, value=20, step=1
    )

    # create an instance of the Sandpile class to use for the simulation
    sandpile = Sandpile(dimension_slider.value)

    # function to schedule periodically; this will be called repeatedly until the simulation is over
    # it will update the sandpile, stream the data, and then stop the callback (if the simulation is over).
    def update_sandpile():
        global sandpile_callback
        sandpile.collapse()
        stream.send(sandpile.sandpile)
        if sandpile.stable:
            sandpile_callback.stop()
            launch_button.name = "Launch!"
            sandpile_callback = None

    # function to tie to the launch button; this resets the sandpile and schedules the simulation
    # this can also pause and unpause the simulation
    def launch(event):
        global sandpile_callback
        if sandpile_callback is not None and sandpile_callback.running:
            sandpile_callback.stop()
            sandpile_callback.running = False
            launch_button.name = "Launch!"
        elif sandpile_callback is not None and not sandpile_callback.running:
            sandpile_callback.start()
            launch_button.name = "Stop!"
        else:
            sandpile.reset(dimension_slider.value)
            sandpile_callback = pn.state.add_periodic_callback(update_sandpile, 50)
            launch_button.name = "Stop!"


    # function to tie to the reset button; this resets the sandpile
    # this will automatically trigger whenever the dimension is changed
    @pn.depends(dimension_slider, watch=True)
    def reset(event):
        global sandpile_callback
        if sandpile_callback is not None:
            sandpile_callback.stop()
        sandpile_callback = None
        sandpile.reset(dimension_slider.value)
        stream.send(sandpile.sandpile)
        launch_button.name = "Launch!"

    # tie the launch and reset functions to their respective buttons
    launch_button.on_click(launch)
    reset_button.on_click(reset)

    # callback to execute whenever we stream data
    def view(data):
        return hv.Image(data)

    # create a data stream for to animate our model data
    stream = hv.streams.Pipe(data=[])

    dmap = hv.DynamicMap(view, streams=[stream]).opts(
        xlim=(-0.5, 0.5),
        ylim=(-0.5, 0.5),
        clim=(0, 4),
        cmap="GnBu",
        xaxis="bare",
        yaxis="bare",
        width=600,
        height=480,
        shared_axes=False,
        show_grid=True,
    )

    return pn.Row(dmap, pn.Column(launch_button, reset_button, dimension_slider))

# main content that we will ultimately inject into the application. Just start appending to it!
main = pn.Column()

main.append(
    pn.pane.Markdown(
        "# HEY, LISTEN! There is some cool stuff loading; be a little patient!",
        max_width=800,
    )
)

main.append(
    markdown(
        f"""# {frontmatter["title"]}

## {frontmatter["date"]}

### {frontmatter["readtime"]} Minutes to Read"""
    )
)

main.append(
    markdown(
        """Now that I am using `panel` as the core of this blog, the doors are blown pretty wide open as far as what can be done (well, this _could_ all be done before, but now _I_ can do it!). I can't possibly cover everything that `panel` does, but take a peek at the [App Gallery](https://panel.holoviz.org/gallery/index.html) to get an idea. It is pretty incredible how easy `panel` makes everything, which is why I was mildly shocked I never thought about doing this sooner.

There are a ton of new opportunities to not only use `panel` to render the markdown (as `geno` was initially written to do), but we can also render `panel` apps using `pyodide`. This means that interactive applications can be written to run in the browser, instead of serving plain HTML/CSS/JS. This gets even crazier if that interactive application in the browser is also utilizing "native" code targeted at WASM. Ultimately I want to write a `panel` app that I can convert to a `pyodide` application, and I want that application to run a C++ library in real-time so that I can visualize the model and some analysis. **All in the browser**.

Let's not get ahead of ourselves... first, we need a way of telling `geno` to simply pull in `panel` applications and get them rendered statically, since all we can do now is render markdown. For a simple `panel` app this is actually quite easy since we are technically doing this already for the markdown pages:

```python
pn.template.BootstrapTemplate(
    # ...
    main=main,
    # ...
).save(page.source_path)
```

We use this call in `geno` with the markdown inserted into the `main` component of the final layout. We can have regular "apps" do the same thing. This is pretty trivial. The thing is, this is giving us more static sites. We cut ourselves off from really benefitting from what `panel` can do! We want to be able to actually run the `panel` application as a post - enter [`pyodide`](https://pyodide.org/en/stable/). This stuff is absolutely voodoo to me - all I know is that `pyodide` is a distribution of Python that targets `WebAssembly` instead of your native system. [`WebAssembly`](https://en.wikipedia.org/wiki/WebAssembly) is also voodoo to me, but I like to think of it as a high-performance runtime that is compatible with your web browser (for better or worse, correct or incorrect, this is how I think of it).

So what does this all mean? This means we can write `panel` applications in Python, and then actually run them in our browser using `pyodide`. This deeply contrasts running Python locally on some machine. You may have noticed some odd loading overlay when you first navigated here - well, this page is actually a `panel` application running with `pyodide` within your browser! This means we can do some pretty nifty things - maybe we can implement a cannon-ball simulation, configure it, and be able to run and visualize it all right here.

## Blast Off!
"""
    )
)

main.append(cannonball_simulation())

main.append(
    markdown(
        """Pretty neat, right? I think so. That model was coded in Python and hooked into `panel` and `holoviews`, **and it is running in your browser**. There are some challenges I am still working through though, largely because I am extremely new to `pyodide` and how it all works with `panel`. Namely, your `pyodide` application cannot embed/use local modules/packages; it must be able to install them (effectively) through [PyPI](https://pypi.org/). This means that your entire application needs to be self-contained. This is less of a roadblock and just some new terrain to map out.
        
You _might_ be thinking that the above example was pretty basic. Well, you're definitely correct there. It is really basic. What about something a little more computationally intense? Well, we have that here too. Here is a simple implementation of the [`Abelian Sandpile Model`](https://en.wikipedia.org/wiki/Abelian_sandpile_model). The implementation here uses `numpy` to setup the sandpile (matrix of integers), and just put every cell at the unstable value of 4. Upon launching the sandpile collapses with a spectacular series of waves (increase the dimension see more)!"""
    )
)

main.append(sandpile_simulation())

main.append(
    markdown(
        """This is running live in your browser! I cannot possibly say that enough; it is so cool! No server is running in the backend, no external services are running, nada. This is such a great first step towards the eventual goal of getting C++ into the mix. There is so much stuff to figure out yet before getting there though. General organization of the apps, the frontmatter, the CSS, etc. are all still ultra-janky. Things clearly work great, but it is all definitely _janky and bad_ and I will be looking at different ways of managing everyting.

## How it Works

`geno` is still in charge of ultimately generating and organizing everything, and that includes this application. Instead of just reading markdown files and throwing them into `panel` components, we also find Python files and use the CLI tool `panel convert` to generate the `pyodide` applications. Internal to `geno` this looks like:

```python
subprocess.run(
    f"panel convert {self.app} --to pyodide-worker --out {self.source_path.parent}".split()
)
```

This takes the `panel` application and runs it through the `pyodide` meat grinder to generate everything necessary to run the application in the browser. Right now I am using a special `<<<css>>>` snippet of text that I do a replacement before the `pyodide` step to use my stylesheets (ick), and I just duplicate the generation of the menu buttons (even more ick). Outside of that, I am just writing a large `panel` application with widgets, plots, plenty of markdown, and lots of ick to just make it work.

## Future

This post is a proof-of-concept to figure out how the main bits and pieces fall into place. It is quite messy, but I am still quite satisfied with the results. The next post (or few) will focus on cleaning up the ick that I added here. I am pretty excited about what is to come!"""
    )
)

# jank
main.append(markdown(f"\n<script>\n    document.title = '{frontmatter['title']} | NESWare.io';</script>"))

# jank
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

# still need to provide a servable object, so this is the final result!
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
