title: Writing My Own Static Site Generator with Panel
section: blog
date: 2025-02-18
tags: python panel
readtime: 3
---fm---

Ever since creating this website a few years ago, I have managed its content and generation using [`Jekyll`](https://jekyllrb.com/). I am not a web developer at all and Jekyll made it all super easy to get started. However, due to my infrequent posting, every time I would come back to write a new post, something about my environment and setup would be broken. I am not a Ruby developer either, so debugging anything was always a tad problematic. The other night I again tried to come back to write new content, and again my environment was broken...

## Trying Hugo

Instead of trying to fix things this time, I figured there surely should be something hot and new to try out. I opted to just test the waters and see what other static-site-generators are available. After a short bit of searching, there seemed to be significant community cheers for [Hugo](https://gohugo.io/). This looked pretty cool, so I gave it a try. It was simple to get going (and it really is fast!), but then I hit a wall of issues that I really had no patience for.

The themes advertised on their website were hit or miss - most themes didn't quite have an aesthetic I was into, and the ones I was interested in seemed to not work quite right. I ran into errors ranging from differing Hugo verisons not working with the theme, all the way to themes straight up not working. I tried to convert content to one theme that seemed promising, but in the end it didn't feel great. I was getting frustrated pretty quickly, and lost interest.

## Panel

I still wanted to replace Jekyll with something, but nothing seemed to stand out to me. As I thought on it a bit more, I figured I would turn to what I know. I am a pretty frequent user of the [Holoviz](https://holoviz.org/) ecosystem when I am developing data analysis and visualization tools, and I am a huge fan of [`Panel`](https://panel.holoviz.org/), a library _"designed to streamline the development of robust tools, dashboards, and complex applications entirely within Python"_. It has default templates for dashboards, and while they are a tad boring for a blog (on the surface), Panel lets us easily inject CSS to style things how we want.

Panel lets you create full-blown dashboards with a large variety of both textual and visual elements, and furthermore also can be rendered to static HTML. You can inject Markdown and CSS directly into Panel, and so at this point I just needed to wrap my blog content into single "dashboard" pages and render them to HTML.

### Features

The current set of features from my new tool are sparse, but it will be acquiring some new skills fairly rapidly over time. I am currently calling it `geno`, named after the one and only Star Road warrior of `Mario RPG`. As of right now I can generate content from markdown, can inject content using some basic frontmatter, and I can automatically deploy to GitHub pages.

In fact, what you are reading this very moment is being hosted from GitHub pages, having been gneerated using `geno`. There is an absolute ton to do to improve `geno` and make it into something others can use, but for now the name of the game is making it whatever I need it to be to better facilitate the addition of new content here.

## Future

With the introduction of `geno` and my new blog, I have cleaned things up a good bit. I removed a number of my old posts, mostly because they are noise and very irrelevant now. I will rehost them eventually as "archives", but I don't care enough right now to really update them with the new paradigms unique to `geno`.

I will be documenting some of the new C++ work I have been doing on the side as well as some RPI and Adafruit tinkering, and as I run through writing those posts I am sure that I will continue to iterate on `geno` and the aesthetic and layout of this website. `geno` lives here in this repository only for now, but will be moving out once it is mature enough and abstracted for general use.
