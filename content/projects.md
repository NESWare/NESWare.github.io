title: Projects
---fm---

## Current Projects

Of course there are always too many things being worked on at any given time, but there are a few projects that in particular are of value that I believe with enough time and effort can actually be something good. I am currently scrubbing down my projects and GitHub to remove what is obsolete (or uninteresting); this should help me focus a bit better in the long run.

{% for page in site.pages.projects %}
- ### [{{ page.title }}]( {{ page.link }})
    - {{ page.tagline }}
{% endfor %}
