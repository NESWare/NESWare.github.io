---
title: Projects
layout: default
---

# Current Projects

Of course there are always too many things being worked on at any given time, but there are a few projects that in particular are of value that I believe with enough time and effort can actually be something good.

---

## Games

<ul>
    {% for project in site.projects %}
        {% if project.category == "game" %}
        <li>
            <h2><a href="{{ project.url }}">{{ project.title }}</a></h2>
       </li>
       {% endif %}
    {% endfor %}
</ul>

## Software

<ul>
    {% for project in site.projects %}
        {% if project.category == "software" %}
        <li>
            <h2><a href="{{ project.url }}">{{ project.title }}</a></h2>
       </li>
       {% endif %}
    {% endfor %}
</ul>
