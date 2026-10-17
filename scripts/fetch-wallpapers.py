#!/usr/bin/env python3
"""Download top-rated 4K Attack on Titan wallpapers from wallhaven.cc for personal use.

The images belong to their artists and studios, so they are fetched to your machine
instead of being shipped in this repository.

usage: fetch-wallpapers.py [--count N] [--dest DIR] [--min 3840x2160] [--exclude ID ...]
"""
import argparse
import json
import os
import sys
import time
import urllib.parse
import urllib.request

API = "https://wallhaven.cc/api/v1/search"
QUERIES = ["attack on titan", "shingeki no kyojin", "levi ackerman", "eren yeager",
           "mikasa ackerman", "survey corps"]
UA = {"User-Agent": "aot-theme-kde/1.0 (+https://github.com/Shubhwtf/aot-theme-kde)"}


def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def search(query, minres, page):
    params = {"q": query, "categories": "010", "purity": "100", "atleast": minres,
              "ratios": "16x9,16x10,21x9,32x9", "sorting": "favorites", "page": page}
    return json.loads(get(f"{API}?{urllib.parse.urlencode(params)}"))["data"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--count", type=int, default=16)
    ap.add_argument("--min", default="3840x2160")
    ap.add_argument("--dest", default=os.path.expanduser("~/.local/share/wallpapers/AttackOnTitan-Collection"))
    ap.add_argument("--exclude", nargs="*", default=["x1xy9l"])  # x1xy9l: multi-anime crossover
    a = ap.parse_args()

    seen, picks = set(a.exclude), []
    for q in QUERIES:
        for page in (1, 2):
            try:
                items = search(q, a.min, page)
            except Exception as e:  # network hiccup or rate limit: move on
                print(f"  search '{q}' failed: {e}", file=sys.stderr)
                break
            for it in items:
                if it["id"] not in seen:
                    seen.add(it["id"])
                    picks.append(it)
            time.sleep(1.5)  # wallhaven allows ~45 requests/minute
            if len(items) < 24:
                break
    picks.sort(key=lambda it: it["favorites"], reverse=True)
    picks = picks[:a.count]

    os.makedirs(a.dest, exist_ok=True)
    for it in picks:
        name = os.path.basename(it["path"])
        out = os.path.join(a.dest, name)
        if os.path.exists(out):
            print(f"  have {name}")
            continue
        print(f"  get  {name}  {it['resolution']}  ♥{it['favorites']}  {it['url']}")
        with open(out + ".part", "wb") as f:
            f.write(get(it["path"]))
        os.replace(out + ".part", out)
        time.sleep(0.5)
    print(f"{len(picks)} wallpapers in {a.dest}")


if __name__ == "__main__":
    main()
