"""Put data.json into template.html and write ../index.html.
Usage: python inject.py data.json
"""
import sys, os
here = os.path.dirname(os.path.abspath(__file__))
t = open(os.path.join(here, "template.html"), encoding="utf-8").read()
d = open(sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "data.json"), encoding="utf-8").read()
assert "/*DATA*/null" in t
open(os.path.join(here, "..", "index.html"), "w", encoding="utf-8").write(t.replace("/*DATA*/null", d))
print("wrote alloys/index.html")
