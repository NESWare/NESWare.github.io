---
title: blog
layout: default
---

# Tags

<ul class="tags">
    {% for tag in site.tags %}
        {% assign t = tag | first %}
        <a href="/tag/#{{t | downcase | replace:" ","-" }}">{{ t | downcase }}</a>
    {% endfor %}
</ul>

## Latest Posts

<ul>
    {% for post in site.posts %}
        <li>
            <h2><a href="{{ post.url }}">{{ post.date | date: "%m/%d/%Y" }} :: {{ post.title }}</a></h2>
       </li>
    {% endfor %}
</ul>
