from collections import namedtuple

Blog = namedtuple("Blog", ["title", "link", "description", ])
Blog.title = "ElCato"
Blog.link = "Welcome to getting started with ElCato"
Blog.image = "./images/me.jpg"
Blog.description = "./images/me.jpg"


Author = namedtuple("Author", ["name", "photo", "blurb", "links"])
Author.name = "El Cato"
Author.blurb = "Welcome to El Cato's blog"
Author.photo = "./images/me.jpg"
Author.links = [
    ["Git", "GitLab", "https://gitlab.com/python-open-source-library-collection/elcato"],
    ["Chat", "Matrix", "https://riot.im/app/#/room/#elcato:matrix.org"],
]
