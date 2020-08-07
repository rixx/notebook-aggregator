import datetime as dt
import json
import pathlib
import subprocess
import time
from functools import partial

import feedparser
from jinja2 import Environment, FileSystemLoader, select_autoescape


def rsync(source, destination):
    subprocess.check_call(["rsync", "--recursive", "--delete", source, destination])


def render_date(date_value):
    if isinstance(date_value, dt.date):
        return date_value.strftime("%Y-%m-%d")
    elif isinstance(date_value, time.struct_time):
        return f"{date_value.tm_year}-{date_value.tm_mon}-{date_value.tm_mday}"
    return date_value


def render_page(template_name, path, env=None, **context):
    template = env.get_template(template_name)
    html = template.render(**context)
    out_path = pathlib.Path("_html") / path
    out_path.parent.mkdir(exist_ok=True, parents=True)
    out_path.write_text(html)


def load_blogs():
    with open("_data/blogs.json") as fp:
        data = json.load(fp)
    return data


def get_date(entry):
    return (
        getattr(entry, "published_parsed", None)
        or getattr(entry, "updated_parsed", None)
        or dt.datetime(1970, 1, 1)
    )


def sort_feed_entries(entries):
    return sorted(entries, key=lambda x: get_date(x), reverse=True)


def get_feed_entries(url):
    data = feedparser.parse(url)
    author = data.feed.get("author", "").split("(")[0].strip()
    for entry in data.entries:
        entry["author"] = entry.get("authors", [{}])[0].get("name") or author
    return sort_feed_entries(data.entries)


def build_site():
    rsync(source="static/", destination="_html/static/")

    env = Environment(
        loader=FileSystemLoader("templates"),
        autoescape=select_autoescape(["html", "xml"]),
    )
    env.filters["render_date"] = render_date

    render = partial(render_page, env=env)

    all_feed_entries = []
    blogs = load_blogs()
    for blog in blogs:
        if feed := blog.get("feed"):
            try:
                feed_entries = get_feed_entries(feed)[:5]
            except Exception as e:
                print(f"Could not get feed for {blog['name']}: {e}")
                continue
            if not feed_entries:
                continue
            all_feed_entries += feed_entries
            blog["last_post"] = feed_entries[0]
            blog["sort_date"] = get_date(feed_entries[0])

    blogs = sorted(
        blogs,
        key=lambda x: (x.get("sort_date") or dt.datetime(1970, 1, 1), x["name"]),
        reverse=True,
    )
    feed_entries = sort_feed_entries(all_feed_entries)

    render(
        "index.html", "index.html", blogs=blogs,
    )

    render(
        "feed.xml", "feed.xml", feed_entries=feed_entries,
    )

    print("✨ Rendered HTML files to _html ✨")
