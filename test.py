# encoding=utf-8

from collections import defaultdict, OrderedDict
import json
from pprint import pprint



string = [{'type': 'PLAY', 'word': '想听'}, {'type': 'ARTIST', 'word': '周华健'}, {'type': 'SONG', 'word': '天涯海角'}]
types = []

slots_types = ["ARTIST", "SONG", "SENTI", "LANG", "THEME", "SCENE", "STYLE"]
slots = []
outer = OrderedDict()
inner = OrderedDict()
for str in string:
    if str['type'] in slots_types:
        slots.append({"name":"{}".format(str['type']), "value":"{}".format(str['word'])})
    elif str['type'] == "RANDOM":
        inner["intent"] = "RANDOM"
        outer["service"] = "musicX"
    elif str['type'] == "PLAY":
        inner["intent"] = "PLAY"
        outer["service"] = "musicX"

inner["slots"] = slots

outer["rc"] = 0
outer["semantic"] = dict(inner)

pprint(dict(outer))

