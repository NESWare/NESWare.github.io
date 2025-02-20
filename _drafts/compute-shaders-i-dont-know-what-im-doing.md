title: Compute Shaders: I don't know what I am doing
section: blog
date: 2025-02-18
tags: c++ gpu opengl compute-shaders
readtime: 20
---fm---

A few weekends ago I decided to start seriously reading about OpenGL and leveraging the GPU for general purpose computing. I have been aware of compute shaders for a long while, but just simply never took the plunge. Afer having spent really only a few hours looking at this stuff, I can confidently say that not only do I know nothing, but that I am also completely blown away by what the GPU can do. I am not so naive to have been unaware of what today's GPUs are capable of, but it was simply _too easy_ to get started for how powerful it is.

## Development Environment

I have been leaning more and more into Conan with CMake, and that is where I started here. I figured out my dependencies, and ended up with dependencies in my `conanfile.py` that look like:

```python
    def requirements(self):
        self.requires("fmt/11.1.1")
        self.requires("nlohmann_json/3.11.3")
        self.requires("opengl/system")
        self.requires("glew/2.2.0")
        self.requires("glfw/3.4")
```

Technically I do not need `fmt` or `nlohmann_json` but they are defaults nowadays whenever I am writing C++. This `conanfile.py` adds the necessary dependencies:

- `opengl`: Core graphics library
- `glew`: Loader for OpenGL and extensions
- `glfw`: Context/window manager

From there I wanted to just try some basic stuff. How can I perform element-wise addition of two `std::vector` objects? Well, this was _easy_. Reading through some documentation and tutorials, I needed to write a *shader* (code for the GPU), manage memory, load/run the shader on the GPU, and lastly retrieve my results.
