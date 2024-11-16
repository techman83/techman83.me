Overhauling techman83.me
========================

```{post} 2017-01-08
:tags: python, personal,
:category: Personal
:author: techman83
```

When I first started this blog [blog](../2014/2014-01-19-first_post.md) in early 2014, I had grand intentions of keeping it up to date. I got a great start forking it from [Paul Fenwick's website](http://pjf.id.au/) which actually provided a solid foundation to build this one.


```{thumbnail} /assets/posts/2017-01-08-overhauling_techman83.me/FormerWebsite.png
:title: New vs Old
:width: 600
:class: figure center
```

For the most part I liked the theme and the layout, however it had some issues. Primarily it was a [Jekyll](https://jekyllrb.com/) based site. Jekyll is an excellent static site generator written in Ruby, which was a problem when the only thing you have Ruby installed for is to generate your website. It also had a number of custom and modified gems written to extend the functionality of the site, which were all committed to the repository along with a bunch of JS libraries. All of that combined meant that I'd upgrade my computer, distro or update and something would break, then I'd have to brush the rust off my Ruby and figure it out. Which ultimately meant it got hard and I lost interest.

Lately I've started to tinker with home automation, python, etc and not having a place to be able to easily share this information was starting to annoy me. Changing to a site generator based in my day-to-day language seemed the best plan, so after playing around with a few I settled on [Pelican](https://blog.getpelican.com/). Whilst I was at it I removed all hard added dependencies and improved the deployment/dependecy update procedures to make it a bunch easier to keep everything up to date.

So here's to a New Year and hopefully lots of content! <3
