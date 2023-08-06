import os
import sys
import yaml
import shutil
import datetime

from elcato.helpers import makefolder, files
from elcato import settings
from elcato.elcato import build
from eorg.parser import parse

# from elcato import build


def init(args):
    path = args.path
    print(settings.ELCATO_ROOT)
    print(path)
    makefolder(path, "")
    makefolder(path, f"posts/")
    makefolder(path, f"site/tags/")
    makefolder(path, f"site/posts/")
    makefolder(path, f"site/images/")
    makefolder(path, f"site/css/")
    makefolder(path, f"site/javascript/")
    shutil.copy(
        f"{settings.ELCATO_ROOT}/posts/org-markup.org", f"{path}/posts/org-markup.org"
    )
    shutil.copy(
        f"{settings.ELCATO_ROOT}/templates/example.yaml", f"{path}/config.yaml"
    )
    shutil.copy(
        f"{settings.ELCATO_ROOT}/templates/media/javascript/elcato.js",
        f"{path}/site/javascript/elcato.js",
    )
    shutil.copy(
        f"{settings.ELCATO_ROOT}/templates/static/default.css",
        f"{path}/site/css/default.css",
    )

    shutil.copy(
        f"{settings.ELCATO_ROOT}/templates/media/me.jpg",
        f"{path}/site/images/me.jpg",
    )
    shutil.copy(
        f"{settings.ELCATO_ROOT}/templates/media/placeholder.jpg",
        f"{path}/site/images/placeholder.jpg",
    )
    shutil.copy(f"{settings.ELCATO_ROOT}/../readme.org", f"{path}/readme.org")
    build(path, path + "/site")


def info(args):
    root = os.path.abspath(args.path)
    if not os.path.exists(root):
        return

    for filename in files(root):
        with open(filename, "r") as fp:
            doc = parse(fp)
            taglist = getattr(doc, "keywords", "").strip().split(":")
            if args.tag is None or args.tag in taglist:
                print(filename + " " + getattr(doc, "title", ""))


def create(args):
    root = os.path.abspath(args.path)
    if not os.path.exists(root):
        return

    path = root + os.sep + args.title + ".org"
    if os.path.exists(path):
        print(f"Exited {path} already exists !")
        return

    now = datetime.datetime.now().isoformat()
    filename = os.path.basename(path)
    folder = os.path.dirname(path)
    # makefolder(args.path, folder)
    with open(path, "w") as fp:
        fp.write(
            f"""
#+TITLE: ElCato Static Blogging Platform
#+DATE: {now}
#+DESCRIPTION:
#+KEYWORDS: colon:split:tags
#+CATEGORY: cato
#+SLUG: slugified-title"""
        )
    print(f"Created {path}")


def build_cmd(args):
    source_path = settings.ROOT
    destination_path = settings.PATH

    config_path = os.path.abspath("./") + os.sep + "config.yaml"
    if os.path.exists(config_path):
        with open(config_path, "r") as fp:
            config = yaml.load(fp)
        siteConfig = config.get("Config", {})
        print(config)
        source_path = siteConfig.get("org_file_path", source_path)
        destination_path = siteConfig.get("output_path", destination_path)
    print(f"Reading org files from {source_path}")
    print(f"Generting files to {destination_path}")
    build(source=source_path, destination=destination_path)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Process some .org files")
    subparsers = parser.add_subparsers(dest="cmd")
    #    parser.add_argument('init', help='Show meta data')
    init_parser = subparsers.add_parser("init", help="Initialize a new blog")
    init_parser.add_argument(
        "-p",
        "--path",
        nargs="?",
        dest="path",
        default="./",
        help="Show meta data",
    )
    init_parser.set_defaults(func=init)

    build_parser = subparsers.add_parser("build", help="secondary options")
    build_parser.set_defaults(func=build_cmd)

    create_parser = subparsers.add_parser("create", help="secondary options")
    create_parser.add_argument(
        "-p",
        "--path",
        dest="path",
        default="./",
        action="store",
        help="Show meta data",
    )
    create_parser.add_argument(
        "-n",
        "--name",
        dest="title",
        action="store",
        help="Name of new blog entry",
    )
    create_parser.set_defaults(name="create", func=create)

    info_parser = subparsers.add_parser("info", help="Info")
    info_parser.add_argument(
        "-t", "--tag", nargs="?", default=None, help="Show meta data"
    )
    info_parser.add_argument(
        "-p",
        "--path",
        dest="path",
        default="./",
        action="store",
        help="Show meta data",
    )
    info_parser.set_defaults(name="info", func=info)

    args = parser.parse_args()
    if args.cmd is None:
        parser.print_usage()
        sys.exit(1)
    args.func(args)


if __name__ == "__main__":
    main()
