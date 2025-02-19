title: Writing Pythonic C++
section: blog
date: 2023-03-11
tags: c++ python
readtime: 25
---fm---

Sometimes you really just need faster code. Before utilizing anything in this post seriously, you should absolutely explore options like `NumPy` and `Numba`, or even `Cython` when you need to write faster Python. There are plenty of highly optimized Python packages to check out! Usually the performance gain from using something like `Numba` or `Cython` is effectively as good as writing native code, but sometimes using those tools is not feasible. While this article will talk specifically about writing C++ as standalone programs, in a later article we will talk about how we can *use* this C++ in our Python programs.

With advances in the C++ language specification we can write C++ easier than ever. Type deduction, brace initialization, and lambdas (and much more) are all features added over the years that make C++ feel so much better. With the help of a few popular open source projects, we can write simple, expressive, and friendly C++ that feels a good bit like Python. At this point we will assume you are using a C++20 compatible compiler - my system currently uses g++ 12.1.0.

*Note #1: I exclusively use C++ for scientific computing/modeling and simulation - this is the lens through which I view C++.*

*Note #2: Some of these techniques are not applicable for writing completely robust software. The goal is to write simple and powerful C++ with as little effort as possible, not to make the most definitively bit-efficient, perfectly encapsulated C++ programs imaginable.*

*Note #3: Some of the proposed techniques here are hotly debated and/or are downright wonky. These techniques work perfectly fine for creating self-contained scientific models, but may not be generally applicable for writing production-grade C++. Do your homework and know what you need.*

* [Features in C++](#features-in-c)
    * [String Formatting](#string-formatting)
    * [Auto](#auto)
    * [Range-Based For-Loops](#range-based-for-loops)
    * [Lambdas](#lambdas)
    * [Ranges](#ranges)
    * [Structs, Default Values, & Brace Initialization](#structs-default-values--brace-initialization)

* [Putting it Together](#putting-it-together)
    * [Python](#python)
    * [C++](#c)
    * [Crude Benchmarking](#crude-benchmarking)

* [Final Notes](#final-notes)

## Features in C++

Let's cover some new (and some not so new) features of C++ that will help us write *simpler C++*.

### String Formatting

A truly fantastic feature of Python is its string formatting. Formatting strings in C++ required using the old `printf` style functions which bring its own set of problems, or the `iomanip` header which is rigid. Fortunately, string formatting was revamped in C++20 with the introduction of the formatting library. Let's compare the Python to C++:

```python
# python
s = f'A circle with radius {circle.radius:.2f} has an area of {area(circle):.4f}'
```

```cpp
// c++
auto s = std::format("A circle with radius {.2f} has an area of {:.4f}", circle.radius, area(circle));
```

The most glaring difference is the presense of f-strings in Python (not needed here, but are used to highlight this difference). Otherwise, string formatting is now largely the same in C++. If your compiler is a bit too old (compiler support for `std::format` has been slow) then you can absolutely turn to [`fmt`](https://github.com/fmtlib/fmt) to handle this for you. In fact, at this point in time though there is still very much every reason to want to use `fmt` over the standard formatting library. In addition to the everything `std::format` does, `fmt` also provides (in addition to quite a few other features):

* named parameters
* formatting collections and ranges

With named parameters we can rewrite the above as:

```cpp
// c++
using namespace fmt::literals;
auto s = fmt::format("A circle with radius {radius:.2f} has an area of {area:.4f}", "radius"_a=circle.radius, "area"_a=area(circle));
```

Still not as good as Python's f-strings, but the format specification looks pretty good now! We can also easily format something like a `std::vector`:

```cpp
// c++
auto s = fmt::format("Test scores: {}", fmt::join(scores, ", "));
```

This delimits the elements of our vector with commas, and correctly *does not* include a trailing comma! While you may not want to print gigantic collections, this can be particularly useful if, say, you are writing a CSV file.

We will use `fmt` and its features for the rest of this article (as needed).

### auto

C++ is statically typed - this means that types for our data must be known at compile-time. This is opposite of Python where everything is dynamically typed at runtime. Introduced in C++11, `auto` is a keyword that tells the compiler to deduce the type for you. While we still need to provide a type, `auto` just tells the compiler to figure it out for us. Compare the following Python and C++ code:

```python
# python
radius = 1.0
```

```cpp
// c++
auto radius = 1.0;
```

The C++ code is slightly longer, but we are able to omit the explicit type for `radius` and allow the compiler to deduce it is a `double`. This does not mean that `radius` is now capable of being rewritten with a different type (as we can in Python) - in our code it is *always* a `double`.

We can use this to great effect though when writing functions so as to create simple generic functions. Again let's check out Python and C++ snippets - let's assume we have some class called `Circle` with a member called `radius`:

```python
# python
def area(circle):
    return math.pi * circle.radius * circle.radius
```

```cpp
// c++
auto area(auto circle) {
    return std::numbers::pi * circle.radius * circle.radius;
}
```

So before we proceed, let's just acknowledge that `area` is a function that should probably live in our `Circle` class, but let's forget this little detail for now. In our C++ version, the compiler deduces that our function `area` returns a `double`, and the context of the function requires that the input has a `radius` member that has multiplication with `doubles` defined. Failure to provide our function with an input that satisfies the requirements of the type would result in a compiler error!

We can use `auto` in a few other key areas to help write simpler code - the goal is not to use it everywhere, but only where it helps us write simple code. Remember that `auto` just tells C++ to figure the type out for you at compile time - you are still responsible for writing code that works (as you always are!), and you should be prepared for potentially nasty compiler errors if the compiler cannot figure things out for you!

### Range-based For-Loops

Conventional for-loops are fairly typical, but can be really verbose when you want to iterate through a collection. One could use iterators, but this is often even more verbose, and with where the language is going, higher level users hardly ever actually need iterators. Range-based for-loops aim to provide a clear and expressive method for writing loops to traverse collections. Let's assume in the following code comparison that we respectively have a list and a vector of integers for Python and C++ and we want to iterate through the elements and print them:

```python
# python
for i in data:
    print(i)
```

```cpp
// c++
for (int i : data) {
    fmt::print("{}\n", i);
}
```

Yes, we could just print the collections directly (in both Python and C++ (via `fmt`)), but this is just a simple example. Furthermore we can *update* a collection in C++ using a range-based for-loop (something we cannot do in Python without using element indices if we have a collection of primitives - specific, but still relevant):

```python
# python
for i, d in enumerate(data):
    data[i] += 1  # or data[i] = d + 1
```

```cpp
// c++
for (int &i : data) {
    i++;
}
```

Here `i` is now a reference to the elements of `data`, so modifying `i` means modifying the contents of `data`. We can do this in Python if the elements are not primitive, but as is it is a little clunky. We can use `auto` as well to write generic code (perhaps in a function with type-deduced arguments):

```cpp
// c++
void increment_data(auto &data) {
    for (auto &i : data) {
        i += 1;  // += is defined for doubles as well, ++ is not
    }
}
```

### Lambdas

Lambdas were introduced with C++11 and with every iteration of the language since they have gotten better for generic programming. Combined with `auto` we can write quick and easy functions just as we can in Python. Lambdas in C++ are certainly a little bit more verbose up front, but most of the syntax is just C++'s function syntax. A *capture* list is introduced that instructs C++ what variables available in the current scope should be captured, or exposed to, the lambda function.

```python
# python
area = lambda circle: math.pi * circle.radius * circle.radius
```

```cpp
// c++
auto area = [](auto circle) {
    return std::numbers::pi * circle.radius * circle.radius;
};
```

The (empty) capture group is denoted by the `[]`, but otherwise this looks just like any other C++ function. C++ deduces the return type of the function for us, though we could be explicit if we wanted to. We use `auto` to help type the lambda itself since it is a generated type. We can use lambdas in all the same ways as we can in Python (though in some cases we may need to put in a little more work). The biggest benefit over Python lambdas is that C++ lambdas can span multiple lines and provide many statements.

### Ranges

This new feature, officially introduced in C++20, is only partially complete. Therefore, we are going to turn to the open source library [range-v3](https://github.com/ericniebler/range-v3). This library forms the basis for the standard ranges library and is mostly compatible.

For those familiar with the Standard Template Library (STL) algorithms provided by C++, you are likely a bit frustrated by the design. If we have a list `data` in Python that we want to sort, it is as simple as writing:

```python
# python
data.sort()
```

But until recently, the equivalent in C++ using `std::vector` would be:

```cpp
// c++
std::sort(data.begin(), data.end());
```

This is extremely clunky. The design exists to allow developers to specify the explicit range over which to perform the operation, but general users mostly just want to apply algorithms to entire containers. This is where `range-v3` comes into play. With `ranges` we can now write the following:

```cpp
// c++
ranges::sort(data);
```

This is *much* better. Even better though is how `range-v3` allows us to compose and chain operations on data both in eager and lazy ways. If we want to transform and sort our data, then we can use the intuitive pipe, `|`,  operator (for brevity we use `ranges`):

```cpp
// c++
using namespace ranges;
auto mod5 = [](auto d){
    return d % 5;
};
data |= actions::transform(mod5) | actions::sort;
```

Actions are eager algorithms while views are lazy algorithms. Most algorithms have both eager and lazy versions, but a few algorithms may not have a lazy verison (like sort). Every algorithm defined by the STL has a `ranges` equivalent in `range-v3` - unfortunately the standard has not yet defined the algorithms from the `numeric` header, and so if you want to have a range equivalent of something like `accumulate` then you need to turn to `range-v3`.

### Structs, Default Values, & Brace Initialization

In C++ a `struct` is just a class where the default access for all members is `public`. We can write our classes in ways that very much feel like Python classes, so long as we follow some rules. One of the more deceptively complicated things to write in C++ are *constructors*. I personally find that I hardly ever really want to write constructors - especially for classes that are mostly just basic payloads (which, for many of the context in which I am coding they are). Obviously this does not mean constructors are bad or that you should never write them. The presence of constructors however prevent us from truly benefiting from *brace initialization*. Let's consider the following Python dataclass and its equivalent C++ class:

```python
# python
@dataclass
class Particle:
    x: float = 0.0
    y: float = 0.0
    vx: float = 0.0
    vy: float = 0.0

    def integrate(self, dt: float) -> None:
        self.x += self.vx * dt
        self.y += self.vy * dt
```

```cpp
// c++
struct Particle {
    double x = 0.0;
    double y = 0.0;
    double vx = 0.0;
    double vy = 0.0;

    void integrate(double dt) {
        x += vx * dt;
        y += vy * dt;
    }
};
```

These implementations really are not that different. Syntax aside our C++ mirrors our Python identically - C++11 introduced default values for class members, and with brace-initialization these default values are used if not specified. Note that in many projects it likely makes sense to separate class method declarations and definitions into source (`.cpp`) and header (`.h`) files, if anything just to help with reducing compilation times. However, defining methods within the class definition can improve general code comprehension. There is an argument to be made that *splitting* the functions into another file also improves general code comprehension, but I struggle to find this to be true 100% of the time. Large classes in Python are not incomprehensible, and the same can be true for C++ classes.

Let's compare some usage of this class (note the use of curly braces in the C++):

```python
# python
p1 = Particle()                      # default initialized
p2 = Particle(1, 2, 3, 4)            # initialized
p3 = Particle(1, 2)                  # partially initialized
p4 = Particle(x=1, y=2, vx=3, vy=4)  # initialized with kwargs
p5 = Particle(vx=3, vy=4)            # partially specified kwargs
```

```cpp
// c++
Particle p1;                             // default initialization
Particle p2 {1, 2, 3, 4};                // brace initialization
Particle p3 {1, 2};                      // partial brace initialization
Particle p4 {.x=1, .y=2, .vx=3, .vy=4};  // designated initialization
Particle p5 {.vx=3, .vy=4};              // partial designated initialization
```

Again the parallels between the Python and C++ code are pretty strong. We can do this in C++ because of a few choices we made when writing our class:

* public members
* no constructors defined or inherited
* no virtual base

This is a simplication of the rules, but is fairly easy to follow. The syntax for designated initialization is a tad bulkier than Python (with the additional periods before each variable name), and the order is strictly enforced, but this is still a massive improvement over conventional arguments in C++. There is more we can do with nested brace initialization and brace-ellision, but what we have so far will certainly suffice.

There are seemingly a million caveats with constructors and brace-initialization; these articles by Arthur O'Dwyer are worth a read if you want to scratch your brain over why C++ is so ridiculous sometimes.

* [Knightmare of Initialization](https://quuxplusone.github.io/blog/2019/02/18/knightmare-of-initialization/)
* [C++20’s parenthesized aggregate initialization has some downsides](https://quuxplusone.github.io/blog/2022/06/03/aggregate-parens-init-considered-kinda-bad/)

## Putting it Together

So we've covered a lot of different topics, and really only scratched the surface of them (not to mention there are many other features not mentioned here!). We have made a number of assumptions with some of the features of C++, but we now know enough to write some fairly Pythonic C++. Let's write a naive brute-force solution to the the n-body problem, or in other words a particle simulation. We will do it in Python and in our Pythonic C++. We will compare some crude runtime metrics to get a rough idea of performance.

We will use some contrived numbers to observe noticeable gravitational forces over a short simulated time, even if it is unrealistic. Because of the difference in random number generators the systems from both languages will not be identical, but that should not change much of anything.

### Python

```python
# python
import csv
import math
import random
from dataclasses import dataclass

GRAVITY = 6.6743e-11  # Newton's Gravitational Constant

@dataclass
class Particle:
    x: float = 0.0
    y: float = 0.0
    vx: float = 0.0
    vy: float = 0.0
    ax: float = 0.0
    ay: float = 0.0
    mass: float = 5.0e6

    def integrate(self, dt: float) -> None:
        self.vx += self.ax * dt
        self.vy += self.ay * dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.ax = 0.0
        self.ay = 0.0

    def add_force(self, other: 'Particle') -> None:
        dx = other.x - self.x
        dy = other.y - self.y
        distance = math.hypot(dx, dy)
        direction = math.atan2(dy, dx)
        force = GRAVITY * other.mass / (distance * distance)
        self.ax += force * math.cos(direction)
        self.ay += force * math.sin(direction)

if __name__ == '__main__':
    num_particles = 500
    particles = [Particle(x=random.uniform(-50.0,50.0), y=random.uniform(-50.0,50.0)) for i in range(num_particles-1)]
    particles.append(Particle(mass=1e12))

    time_delta = 0.1
    simulation_time = 0.0
    max_simulation_time = 50.0

    with open('particles.csv', 'w', newline='') as csvfile:
        sim_writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        while simulation_time < max_simulation_time:
            for p1 in particles:
                for p2 in particles:
                    if p1 is p2: continue
                    p1.add_force(p2)
            for p1 in particles:
                p1.integrate(time_delta)
                sim_writer.writerow(['{:.8f}'.format(d) for d in [simulation_time, p1.mass, p1.x, p1.y]])
            simulation_time += time_delta
```

### C++

```cpp
// c++
#include <cmath>
#include <fstream>
#include <random>
#include <vector>
#include <fmt/format.h>
#include <fmt/ostream.h>

constexpr double GRAVITY = 6.6743e-11;  // Newton's Gravitational Constant

struct Particle {
    double x = 0.0;
    double y = 0.0;
    double vx = 0.0;
    double vy = 0.0;
    double ax = 0.0;
    double ay = 0.0;
    double mass = 5.0e6;

    void integrate(const double dt) {
        vx += ax * dt;
        vy += ay * dt;
        x += vx * dt;
        y += vy * dt;
        ax = 0.0;
        ay = 0.0;
    }

    void add_force(const Particle &other) {
        double dx = other.x - x;
        double dy = other.y - y;
        double distance = std::hypot(dx, dy);
        double direction = std::atan2(dy, dx);
        double force = GRAVITY * other.mass / (distance * distance);
        ax += force * std::cos(direction);
        ay += force * std::sin(direction);
    }
};

int main() {
    std::mt19937 eng;
    std::uniform_real_distribution<double> dis(-50.0, 50.0);

    int num_particles = 1000;
    std::vector<Particle> particles;
    particles.reserve(num_particles);
    for (auto i = 0; i < num_particles-1; ++i) {
        particles.emplace_back(dis(eng), dis(eng));
    }
    particles.emplace_back(0, 0, 0, 0, 0, 0, 1e12);

    double time_delta = 0.1;
    double simulation_time = 0.0;
    double max_simulation_time = 50.0;

    std::ofstream csvfile("particles.csv");
    while (simulation_time < max_simulation_time) {
        for (auto &p1 : particles) {
            for (const auto &p2 : particles) {
                if (&p1 == &p2) continue;
                p1.add_force(p2);
            }
        }
        for (auto &p1 : particles) {
            p1.integrate(time_delta);
            fmt::print(csvfile, "{:.8f},{:.8f},{:.8f},{:.8f}\n", simulation_time, p1.mass, p1.x, p1.y);
        }
        simulation_time += time_delta;
    }
}
```

### Crude Benchmarking

On my system the Python model takes ~1m:55s to simulate 500 particles for 50 seconds with model updates at 10Hz. This time includes writing the data to a CSV. On the same system the C++ model takes about ~0m:8.5s. Enabling compiler optimization (O2) brings it down to ~0m:6s, and enabling aggressive optimization (O3) brings it down a tiny bit to (barely) <0m:6s. While runtime is not really a great metric to just benchmark alone on, the speed improvements are too significant to ignore.

However, comparing raw Python to raw C++ is not entirely fair considering that anyone writing scientific code is likely also using `NumPy`. We can rewrite our simulation using a more data-oriented design - by using `NumPy` arrays and `Numba` to JIT some of the code the model takes ~0m:8.5s to simulate the same system, effectively as fast as our raw unoptimized C++! Regardless of the performance we are getting from Python, our optimized C++ model performs best.

### Numpy + Numba

```python
import csv
import numba as nb 
import numpy as np 
from numba import float64

GRAVITY = 6.6743e-11  # Newton's Gravitational Constant

if __name__ == '__main__':
    num_particles = 500
    position = np.random.uniform(-50.0,50.0, size=(num_particles, 2)).astype(np.float64)
    velocity = np.zeros((num_particles, 2), dtype=np.float64)
    mass = np.full(num_particles, 5e6, dtype=np.float64)
    position[0,:] = [0.0, 0.0]
    mass[0] = 1e12

    @nb.guvectorize([(float64[:,:], float64[:,:])], '(n,m)->(n,m)', boundscheck=False, fastmath=True, nopython=True)
    def get_accelerations(p, a):
        for i in range(p.shape[0]):
            diffs = position - p[i]
            distances = np.hypot(diffs[:,0], diffs[:,1])
            direction = np.arctan2(diffs[:,1], diffs[:,0])
            force = GRAVITY * mass / (distances * distances)
            force[i] = 0.0
            force_x = np.nansum(force * np.cos(direction))
            force_y = np.nansum(force * np.sin(direction))
            a[i,:] = [force_x, force_y]

    time_delta = 0.1
    simulation_time = 0.0
    max_simulation_time = 50.0

    with open('particles.csv', 'w', newline='') as csvfile:
        sim_writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        while simulation_time < max_simulation_time:
            simulation_time += time_delta
            velocity += get_accelerations(position) * time_delta
            position += velocity * time_delta
            for (m, p) in zip(mass, position):
                sim_writer.writerow(['{:.8f}'.format(d) for d in [simulation_time, m, *p]])
```


## Final Notes

I will reiterate that the goal is to write simple, expressive, and friendly C++. C++ can be rough around the edges, but it does not need to be impossible to get your feet wet. The language has come a long way in recent years, and deserves another look if you've been away from it for a while.
