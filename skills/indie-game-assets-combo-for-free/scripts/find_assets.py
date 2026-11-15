#!/usr/bin/env python3
"""Route free asset searches and query Poly Haven and Godot catalogs."""
import argparse
import json
import re
import sys
from urllib.error import URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen


SOURCES = {
    "kenney": ("Kenney", "https://kenney.nl/assets", "web"),
    "opengameart": ("OpenGameArt", "https://opengameart.org/art-search-advanced", "web"),
    "itch": ("itch.io", "https://itch.io/game-assets/free", "web"),
    "unity": ("Unity Asset Store", "https://assetstore.unity.com/top-assets/top-free", "manual"),
    "fab": ("Fab", "https://www.fab.com/search", "web"),
    "godot": ("Godot", "https://store.godotengine.org/search/", "api+web"),
    "poly-haven": ("Poly Haven", "https://polyhaven.com/assets", "api+web"),
    "mixamo": ("Mixamo", "https://www.mixamo.com/", "manual"),
    "freesound": ("Freesound", "https://freesound.org/search/", "web"),
    "pixabay": ("Pixabay", "https://pixabay.com/", "web"),
}
TYPES = {
    "2d": ("kenney", "opengameart", "itch", "unity", "fab", "godot"),
    "3d": ("poly-haven", "kenney", "fab", "itch", "opengameart", "unity", "godot"),
    "animation": ("mixamo", "itch", "fab", "unity", "opengameart", "kenney"),
    "fonts": ("itch", "opengameart", "kenney", "unity"),
    "hdri": ("poly-haven", "fab", "unity"),
    "image": ("pixabay", "opengameart", "itch"),
    "materials": ("poly-haven", "fab", "opengameart", "kenney", "unity"),
    "music": ("pixabay", "opengameart", "itch", "freesound", "fab", "unity"),
    "plugins": ("godot", "unity", "fab", "itch"),
    "sfx": ("freesound", "kenney", "pixabay", "opengameart", "itch", "unity", "fab"),
    "ui": ("kenney", "itch", "opengameart", "unity", "godot", "fab"),
    "vfx": ("kenney", "itch", "fab", "unity", "opengameart", "godot"),
    "video": ("pixabay",),
}
ITCH_TAGS = {
    "2d": "2d", "3d": "3d", "animation": "animation", "fonts": "fonts",
    "music": "music", "sfx": "sound-effects", "ui": "user-interface",
}
KENNEY_CATEGORIES = {
    "2d": "2D", "3d": "3D", "materials": "Textures", "sfx": "Audio", "ui": "2D",
}
PIXABAY_PATHS = {"image": "images", "video": "videos", "music": "music", "sfx": "sound-effects"}
POLY_TYPES = {"3d": "models", "materials": "textures", "hdri": "hdris"}
POLY_API = "https://api.polyhaven.com/"
GODOT_STORE_API = "https://store.godotengine.org/api/v1/"
GODOT_LEGACY = "https://godotengine.org/asset-library/"
USER_AGENT = "indie-game-assets-combo-for-free/1.0"


def route_for(source, kind, query):
    name, url, access = SOURCES[source]
    route = {"id": source, "source": name, "access": access}
    if source == "fab":
        params = {"is_free": 1}
        if query:
            params["q"] = query
        url += "?" + urlencode(params)
    elif source in ("kenney", "opengameart", "godot", "freesound"):
        keys = {"kenney": "search", "opengameart": "keys", "godot": "query", "freesound": "q"}
        if source == "kenney" and kind in KENNEY_CATEGORIES:
            url += "/category:" + KENNEY_CATEGORIES[kind]
        if query:
            url += "?" + urlencode({keys[source]: query})
        if source == "godot":
            route["legacy_url"] = GODOT_LEGACY + "asset"
    elif source == "itch":
        if kind in ITCH_TAGS:
            url += "/tag-" + ITCH_TAGS[kind]
        if query:
            route["keyword_search_all_prices"] = "https://itch.io/search?" + urlencode({"q": query})
    elif source == "pixabay" and kind in PIXABAY_PATHS:
        url += PIXABAY_PATHS[kind] + "/"
        if query:
            url += "search/" + quote(query, safe="") + "/"
    elif source == "poly-haven" and kind in POLY_TYPES:
        url = "https://polyhaven.com/" + POLY_TYPES[kind]
    route["url"] = url
    return route


def request_json(url):
    headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    with urlopen(Request(url, headers=headers), timeout=15) as response:
        return json.load(response)


def poly_search(args):
    params = urlencode({"q": args.query, "t": POLY_TYPES[args.type]})
    data = request_json(POLY_API + "search?" + params)
    results = []
    for match in data["results"][:args.limit]:
        slug = match["slug"]
        results.append({
            "slug": slug,
            "score": match.get("score"),
            "page": "https://polyhaven.com/a/" + quote(slug, safe=""),
        })
    return {"source": "Poly Haven", "asset_license": "CC0", "results": results}


def poly_files(args):
    files = request_json(POLY_API + "files/" + args.slug)
    return {"source": "Poly Haven", "page": "https://polyhaven.com/a/" + args.slug, "files": files}


def godot_search(args):
    if args.legacy:
        return godot_legacy_search(args)
    params = {"query": args.query, "compatibility": args.version, "require_release": "true"}
    if args.kind != "any":
        params["type"] = 0 if args.kind == "addon" else 1
    data = request_json(GODOT_STORE_API + "search/query/?" + urlencode(params))
    results = []
    for hit in data["hits"]:
        item = hit["asset"]
        if item["price_cent"] != 0:
            continue
        results.append({
            "title": item["name"],
            "author": item["publisher"]["name"],
            "listing_license": item["license_type"],
            "license_url": item["license_url"],
            "page": item["store_url"],
        })
    return {
        "source": "Godot Asset Store",
        "requested_godot_version": args.version,
        "results": results[:args.limit],
    }


def godot_legacy_search(args):
    params = urlencode({
        "type": args.kind,
        "filter": args.query,
        "godot_version": args.version,
        "max_results": args.limit,
    })
    data = request_json(GODOT_LEGACY + "api/asset?" + params)
    results = []
    for item in data["result"]:
        asset_id = item["asset_id"]
        results.append({
            "id": asset_id,
            "title": item["title"],
            "author": item["author"],
            "category": item["category"],
            "listing_license": item["cost"],
            "listed_godot_version": item["godot_version"],
            "asset_version": item["version_string"],
            "page": GODOT_LEGACY + "asset/" + str(asset_id),
            "detail_api": GODOT_LEGACY + "api/asset/" + str(asset_id),
        })
    return {
        "source": "Godot Asset Library (legacy)",
        "requested_godot_version": args.version,
        "total_items": data["total_items"],
        "results": results,
    }


def nonempty(value):
    value = value.strip()
    if not value:
        raise argparse.ArgumentTypeError("enter a non-empty value")
    return value


def limit(value):
    number = int(value)
    if not 1 <= number <= 50:
        raise argparse.ArgumentTypeError("limit must be between 1 and 50")
    return number


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    route = commands.add_parser("route", help="print search entry points without network requests")
    route.add_argument("type", choices=("all", *TYPES))
    route.add_argument("query", nargs="?", default="")
    route.add_argument("--source", choices=SOURCES)

    poly = commands.add_parser("poly-search", help="search the live Poly Haven catalog")
    poly.add_argument("type", choices=POLY_TYPES)
    poly.add_argument("query", type=nonempty)
    poly.add_argument("--limit", type=limit, default=5)

    files = commands.add_parser("poly-files", help="list files for a Poly Haven asset slug")
    files.add_argument("slug")

    godot = commands.add_parser("godot-search", help="search the first page of the Godot Asset Store")
    godot.add_argument("query", type=nonempty)
    godot.add_argument("--version", type=nonempty, required=True)
    godot.add_argument("--kind", choices=("any", "addon", "project"), default="any")
    godot.add_argument("--legacy", action="store_true", help="query the earlier Godot Asset Library")
    godot.add_argument("--limit", type=limit, default=5)

    args = parser.parse_args()
    if args.command == "poly-files" and not re.fullmatch(r"[a-z0-9_-]+", args.slug):
        parser.error("use the asset slug returned by poly-search")
    if args.command == "godot-search" and not re.fullmatch(r"\d+\.\d+(?:\.\d+)?", args.version):
        parser.error("use a Godot version such as 4.4 or 4.4.1")

    if args.command == "route":
        sources = (args.source,) if args.source else TYPES.get(args.type, SOURCES)
        query = args.query.strip()
        result = {
            "type": args.type,
            "query": query,
            "routes": [route_for(source, args.type, query) for source in sources],
        }
    else:
        handlers = {"poly-search": poly_search, "poly-files": poly_files, "godot-search": godot_search}
        try:
            result = handlers[args.command](args)
        except (URLError, TimeoutError, ValueError, KeyError, TypeError) as exc:
            print(f"{args.command} failed: {exc}. Use route for the website entry point.", file=sys.stderr)
            return 1

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
