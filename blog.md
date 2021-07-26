---
title: Blog
layout: default
---

# Latest Posts

Look around, you might, though unlikely, find something you like!

---
<ul>
    {% for post in site.posts %}
        <li>
            <h2><a href="{{ post.url }}">{{ post.date | date: "%m/%d/%Y" }} :: {{ post.title }}</a></h2>
       </li>
    {% endfor %}
</ul>
