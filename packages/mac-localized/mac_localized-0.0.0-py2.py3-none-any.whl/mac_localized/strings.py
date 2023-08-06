#!/usr/bin/env python
import os
import public

"""
Folder.localized/.localized/de.strings:
"Folder" = "Translation";
"""


def find(path):
    result = []
    for f in os.listdir(path):
        name, ext = os.path.splitext(f)
        if ext == ".strings":
            fullpath = os.path.join(path, f)
            result.append(fullpath)
    return result


def load(path):
    for s in filter(lambda s: " = " in s, open(path).read().splitlines()):
        key = s.split(" = ")[0].replace('"', '')
        value = s.split(" = ")[1].replace('"', '').replace(';', '').rstrip()
        return key, value


def update(path, key, value):
    string = '"%s" = "%s";\n' % (key, value)
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    open(path, "w").write(string)
