import os
import json
import yaml
import shutil
from dotenv import load_dotenv
from collections import namedtuple
from feedgen.feed import FeedGenerator
from atom.api import Atom, Unicode, Bool, Enum

from eorg.parser import parse
from eorg.generate import html
from eorg import const
import eorg

from elcato.helpers import images, makefolder, files
from elcato.templates.enaml.template import viewIndex, viewPage
from elcato.data import Blog, Author
from elcato import settings


def build_feed(path):
    fg = FeedGenerator()
    fg.id('http://lernfunk.de/media/654321')
    fg.title(Blog.title)
    fg.author( {'name': Author.name,'email':'john@example.de'} )
    fg.logo(Blog.image)
    fg.subtitle(Blog.description)
    fg.link( href=Blog.link, rel='self' )
    fg.language('en')
    fg.rss_file(f'{path}/rss.xml')


#def init(path):
#    makefolder(path, f"tags/")
#    makefolder(path, f"posts/")
#    makefolder(path, f"images/")


def build(source, destination):
    tags = {}
    cards = []
    pages = {}

    pos = 0
    for filename in files(source):
        print(f"#### Processing {filename}")
        doc = []
        with open(filename, "r") as fp:
            doc = parse(fp)
            cards.append(doc)
            pages[doc.title.strip()] = doc.slug.strip()
            #pages[pos] = {'id': pos, 'text': doc.title}

            taglist = doc.keywords.strip().split(":")
            for tag in taglist:
                tags.setdefault(tag.strip(), []).append(filename)
                images(source, destination, doc)
                filename = os.path.basename(filename)
            with open(f"{destination}/posts/{doc.slug.strip()}.html", "wb") as f:
                f.write(
                    viewPage.render(title=doc.title, doc=doc, body=html(doc).read())
                )
        pos += 1
    with open(f"{destination}/index.html", "wb") as f:
        f.write(viewIndex.render(title="Index", cards=cards, author=Author))

    with open(f"{destination}/tags/all.json", "w") as f:
        json.dump(tags, f)

    with open(f"{destination}/tags/search.js", "w") as f:
        f.write('var searchData = ')
        json.dump(pages, f)
        f.write(';')
        f.write("var elcatoSearch = M.Autocomplete.getInstance(document.querySelector('#search'));")
        f.write('elcatoSearch.updateData(searchData);')




    for key, value in tags.items():
        key = key.strip()
        with open(f"{destination}/tags/{key}.json", "w") as f:
            f.write('var searchData = ')
            json.dump(tags[key], f)
            f.write(';')


if __name__ == "__main__":
    source_path = settings.ROOT
    destination_path = settings.PATH

    config_path = os.path.abspath('./') + os.sep + 'config.yaml'
    if os.path.exists(config_path):
        with open(config_path, 'r') as fp:
            config = yaml.load(fp)
        source_path = config.org_file_path
    print(f'Reading org files from {source_path}')
    print(f'Generting files to {destination_path}')

    #init(settings.PATH)
    build(source=source_path, destination=destination_path)
    #build(settings.ROOT, settings.PATH)
    build_feed(settings.PATH)
