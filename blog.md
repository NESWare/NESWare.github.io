---
title: blog
layout: default
---

<h1>Tags</h1>

<ul class="tags">
{% for tag in site.tags %}
    {% assign t = tag | first %}
    {% assign posts = tag | last %}
    <li>{{t | downcase | replace:" ","-" }} has {{ posts | size }} posts</li>
{% endfor %}
</ul>

<h1>Latest Posts</h1>

<ul>
  {% for post in site.posts %}
    <li>
      <h2><a href="{{ post.url }}">{{ post.date | date: "%m/%d/%Y" }} :: {{ post.title }}</a></h2>
    </li>
  {% endfor %}
</ul>
