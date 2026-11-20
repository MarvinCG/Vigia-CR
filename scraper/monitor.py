"""Monitor de seguridad pública y sistema penitenciario de Costa Rica.

Corre sin dependencias externas (solo librería estándar de Python 3.10+).
Uso:  python scraper/monitor.py            -> busca en internet y actualiza data/items.json
      python scraper/monitor.py --fixture  -> usa datos de ejemplo (para probar sin red)
"""
from __future__ import annotations

import hashlib
import html
import json
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import config  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
ITEMS_FILE = DATA / "items.json"
PAGES_FILE = DATA / "pages_state.json"
UA = "Mozilla/5.0 (VigiaCR monitor ciudadano; +https://github.com)"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def fetch(url: str, timeout: int = 25) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def clean(text: str) -> str:
    text = html.unescape(re.sub(r"<[^>]+>", " ", text or ""))
    return re.sub(r"\s+", " ", text).strip()


def google_news(query: str) -> list[dict]:
    q = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={q}+when:30d&hl=es-419&gl=CR&ceid=CR:es-419"
    root = ET.fromstring(fetch(url))
    out = []
    for it in root.iter("item"):
        title = clean(it.findtext("title", ""))
        link = it.findtext("link", "")
        source = clean(it.findtext("source", ""))
        desc = clean(it.findtext("description", ""))
        try:
            date = parsedate_to_datetime(it.findtext("pubDate", "")).astimezone(timezone.utc).isoformat()
        except Exception:
            date = now_iso()
        out.append({"title": title, "url": link, "source": source, "summary": desc, "date": date})
    return out[: config.MAX_PER_QUERY]


def classify(item: dict) -> dict:
    text = f"{item['title']} {item.get('summary', '')}".lower()
    topics = sorted({label for kw, label in config.TOPICS.items() if kw in text})
    signals = sorted({s for s in config.CONTRADICTION_SIGNALS if s in text})
    item["topics"] = topics
    item["signals"] = signals
    # Puntaje simple: señales normativas pesan más si coinciden con temas penitenciarios
    item["score"] = len(signals) * 2 + len(topics)
    item["flag"] = len(signals) >= 2 or (len(signals) >= 1 and bool(topics))
    return item


def item_id(url: str, title: str) -> str:
    return hashlib.sha1(f"{title.lower()}|{url}".encode()).hexdigest()[:16]


def load(path: Path, default):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return default


def check_pages(state: dict) -> list[dict]:
    """Detecta cambios en páginas oficiales comparando un hash del texto visible."""
    new = []
    for cat, name, url in config.WATCH_PAGES:
        try:
            text = clean(fetch(url).decode("utf-8", "ignore"))
        except Exception as e:
            print(f"  ! no se pudo leer {url}: {e}")
            continue
        h = hashlib.sha256(text.encode()).hexdigest()
        if state.get(url) and state[url] != h:
            new.append({
                "title": f"Cambio detectado en: {name}",
                "url": url, "source": name, "date": now_iso(), "category": cat,
                "summary": "La página oficial cambió desde la última revisión. Revise si hay un documento nuevo.",
            })
        state[url] = h
    return new


def run(fixture: bool = False) -> None:
    DATA.mkdir(exist_ok=True)
    items = {i["id"]: i for i in load(ITEMS_FILE, {"items": []})["items"]}
    found: list[dict] = []

    if fixture:
        found = json.loads((ROOT / "scraper" / "fixture.json").read_text(encoding="utf-8"))
    else:
        for cat, q in config.QUERIES:
            try:
                for r in google_news(q):
                    r["category"] = cat
                    r["query"] = q
                    found.append(r)
                print(f"  ok  {q}")
            except Exception as e:
                print(f"  !   {q}: {e}")
        state = load(PAGES_FILE, {})
        found += check_pages(state)
        PAGES_FILE.write_text(json.dumps(state, indent=1), encoding="utf-8")

    added = 0
    for r in found:
        iid = item_id(r["url"], r["title"])
        if iid in items:
            continue
        r["id"] = iid
        r["first_seen"] = now_iso()
        items[iid] = classify(r)
        added += 1

    ordered = sorted(items.values(), key=lambda i: i.get("date", ""), reverse=True)[: config.MAX_ITEMS]
    payload = {
        "updated": now_iso(),
        "count": len(ordered),
        "flagged": sum(1 for i in ordered if i.get("flag")),
        "items": ordered,
    }
    ITEMS_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Nuevos: {added} | Total: {len(ordered)} | Para revisar: {payload['flagged']}")


if __name__ == "__main__":
    run(fixture="--fixture" in sys.argv)
