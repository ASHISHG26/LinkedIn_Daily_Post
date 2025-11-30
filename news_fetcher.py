# fetch_ai_news.py

import feedparser
import re
import random
from datetime import datetime, timedelta
from typing import List

# --------- INDIA FOCUSED FEEDS ---------

INDIA_AI_DATA_FEEDS = [
    "https://analyticsindiamag.com/feed/feed",
    "https://www.analyticsvidhya.com/rss.xml",
    "https://indiaai.gov.in/news/all",
    "https://www.expresscomputer.in/feed/",
    "https://www.dqindia.com/feed/",
]

INDIA_STARTUP_FEEDS = [
    "https://inc42.com/feed/",
    "https://yourstory.com/feed",
    "https://economictimes.indiatimes.com/tech/startups/rssfeedsection.cms",
    "https://www.livemint.com/rss/technology",
    "https://www.moneycontrol.com/rss/technology.xml",
]

INDIA_HARDWARE_TECH_FEEDS = [
    "https://www.gadgets360.com/rss/latest",
    "https://www.gadgets360.com/rss/mobiles",
    "https://www.gadgets360.com/rss/pc",
    "https://indianexpress.com/section/technology/feed/",
    "https://www.91mobiles.com/feed",
    "https://www.hindustantimes.com/rss/tech/news",
]

INDIA_IT_BUSINESS_TECH = [
    "https://timesofindia.indiatimes.com/technology/rssfeedsection.cms",
    "https://www.thehindubusinessline.com/info-tech/feeder/default.rss",
    "https://www.business-standard.com/rss/technology-102.rss",
    "https://www.financialexpress.com/industry/technology/feed/",
]

# --------- GLOBAL BACKUP FEEDS ---------

GLOBAL_AI_FEEDS = [
    "https://feeds.feedburner.com/TechCrunch/artificial-intelligence",
    "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
    "https://www.technologyreview.com/feed/tag/artificial-intelligence/",
    "https://www.wired.com/feed/tag/ai/latest/rss",
]

# --------- COMBINED CATEGORIES ---------

CATEGORIES = {
    "AI_INDIA": INDIA_AI_DATA_FEEDS,
    "STARTUP_INDIA": INDIA_STARTUP_FEEDS,
    "HARDWARE_INDIA": INDIA_HARDWARE_TECH_FEEDS,
    "IT_BUSINESS_INDIA": INDIA_IT_BUSINESS_TECH,
    "GLOBAL_AI": GLOBAL_AI_FEEDS,
}

# --------- HELPERS ---------

TAG_RE = re.compile(r"<[^>]+>")


def _clean_html(text):
    if not text:
        return ""
    return TAG_RE.sub("", text).replace("\n", " ").strip()


def _is_recent(entry, days=4):
    pub = getattr(entry, "published_parsed", None)
    if not pub:
        return True  # Keep if no timestamp
    published_dt = datetime(*pub[:6])
    return (datetime.now() - published_dt).days <= days


# --------- MAIN FETCH FUNCTION ---------

def fetch_ai_news(max_items=4, max_age_days=4):
    """ Fetch 3–4 fresh tech/AI/DE/startup stories with Indian bias. """

    # Pick a random Indian-first category (AI / Data / Startup / Hardware / IT)
    weights = {
        "AI_INDIA": 3,
        "STARTUP_INDIA": 3,
        "HARDWARE_INDIA": 2,
        "IT_BUSINESS_INDIA": 2,
        "GLOBAL_AI": 1,
    }

    categories = list(CATEGORIES.keys())
    chosen_category = random.choices(categories, weights=[weights[c] for c in categories])[0]

    feeds = CATEGORIES[chosen_category]
    print(f"[News] Selected category: {chosen_category}")

    collected = []

    # Parse feeds
    for url in feeds:
        try:
            feed = feedparser.parse(url)
        except Exception:
            continue

        for entry in feed.entries[:12]:  # scan deeper for variety
            if not _is_recent(entry, max_age_days):
                continue

            title = entry.get("title", "").strip()
            if not title:
                continue

            summary = _clean_html(entry.get("summary") or entry.get("description") or "")
            summary = summary[:260]

            link = entry.get("link", "")

            collected.append({
                "title": title,
                "summary": summary,
                "link": link,
                "region": chosen_category,
            })

    if not collected:
        return ""

    # Deduplicate
    seen = set()
    unique = []
    for item in collected:
        key = item["title"].lower()
        if key not in seen:
            seen.add(key)
            unique.append(item)

    # Shuffle and pick final
    random.shuffle(unique)
    final_items = unique[:max_items]

    # Format — LLM-ready context
    lines = []
    for it in final_items:
        region = "India" if "INDIA" in it["region"] else "Global"
        if it["summary"]:
            lines.append(f"- [{region}] {it['title']}: {it['summary']}")
        else:
            lines.append(f"- [{region}] {it['title']}")

    return "\n".join(lines)


# Debug test
if __name__ == "__main__":
    print(fetch_ai_news())