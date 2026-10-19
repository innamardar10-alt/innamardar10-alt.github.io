"""Собирает RSS-ленту для Postmypost из posts/posts.json.

Как работает конвейер:
1. Новый пост добавляется в posts/posts.json (свежие сверху).
2. Запускается: python3 posts/build_feed.py
3. Получается файл rss.xml в корне сайта:
   https://innamardar10-alt.github.io/rss.xml
4. Postmypost проверяет ленту и кладёт новые посты в черновики.

Postmypost берёт только записи не старше суток и картинку только из <enclosure>.
Поэтому у каждого поста должны быть дата (date) и картинка (image) сразу.
"""

import json
import pathlib
from datetime import datetime
from email.utils import format_datetime
from xml.sax.saxutils import escape

ROOT = pathlib.Path(__file__).resolve().parent.parent
POSTS = ROOT / "posts" / "posts.json"
FEED = ROOT / "rss.xml"
SITE = "https://innamardar10-alt.github.io"
MAX_ITEMS = 20


def cdata(text: str) -> str:
    return "<![CDATA[" + text.replace("]]>", "]]]]><![CDATA[>") + "]]>"


def build() -> None:
    posts = json.loads(POSTS.read_text(encoding="utf-8"))
    posts.sort(key=lambda p: p["date"], reverse=True)

    items = []
    for p in posts[:MAX_ITEMS]:
        body = p["text"].strip()
        if p.get("cta"):
            body += "\n\n" + p["cta"].strip()
        pub = format_datetime(datetime.fromisoformat(p["date"]))
        image = p["image"]
        mime = "image/png" if image.lower().endswith(".png") else "image/jpeg"
        items.append(
            "    <item>\n"
            f"      <title>{escape(p['title'])}</title>\n"
            f"      <description>{cdata(body)}</description>\n"
            f'      <guid isPermaLink="false">{escape(p["id"])}</guid>\n'
            f"      <pubDate>{pub}</pubDate>\n"
            f'      <enclosure url="{escape(image)}" type="{mime}" length="0"/>\n'
            "    </item>"
        )

    now = format_datetime(datetime.now().astimezone())
    feed = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
        "  <channel>\n"
        "    <title>Посты про Авито</title>\n"
        f"    <link>{SITE}/</link>\n"
        "    <description>Посты для Postmypost</description>\n"
        "    <language>ru</language>\n"
        f"    <lastBuildDate>{now}</lastBuildDate>\n"
        f'    <atom:link href="{SITE}/rss.xml" rel="self" type="application/rss+xml"/>\n'
        + "\n".join(items)
        + "\n  </channel>\n</rss>\n"
    )
    FEED.write_text(feed, encoding="utf-8")
    print(f"rss.xml: {len(items)} пост(ов)")


if __name__ == "__main__":
    build()
