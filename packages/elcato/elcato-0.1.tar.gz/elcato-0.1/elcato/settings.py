import os
from dotenv import load_dotenv
from eorg import const

load_dotenv()

ELCATO_ROOT = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.abspath(os.environ.get("DESTINATION_FILES", default="./output/"))
ROOT = os.path.abspath("../../do-blog/posts/")


# Start regex, End regex, skip start, skip end, count matches
const.METADATA = [
    "TITLE",
    "AUTHOR",
    "EMAIL",
    "DESCRIPTION",
    "KEYWORDS",
    "SLUG",
    "THUMBNAIL",
    "CATEGORY",
    "DATE",
]
const.t_META = r"^[#]\+(" + "|".join(const.METADATA) + ")\:"
const.TOKENS["META"] = (const.t_META, False, 2, -1, False)
