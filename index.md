---
title: home
layout: default
---

# Home

NESWare is my creative and professional outlet for all things code! This site is a work in progress, but *an active work in progress*!

{% for post in site.posts %}
{% unless post.draft %}
<article class="post">    

    <h1><a href="{{ site.baseurl }}{{ post.url }}">{{ post.title }}</a></h1>

    {{ post.content | split:"<!--more-->" | first }} ... 

    <a href="{{ site.baseurl }}{{ post.url }}" class="read-more">read more</a>

{% endunless %}
{% endfor %}
