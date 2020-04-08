---
title: blog
layout: default
---

# Latest Posts

<ul>
    {% for post in site.posts %}
        <li>
            <h2><a href="{{ post.url }}">{{ post.date | date: "%m/%d/%Y" }} :: {{ post.title }}</a></h2>
       </li>
    {% endfor %}
</ul>
