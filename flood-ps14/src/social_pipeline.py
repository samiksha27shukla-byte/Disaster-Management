"""Keyword-based social media distress signal extraction (synthetic posts)."""
import re
import random

KEYWORDS = {"flood": 1.0, "water rising": 1.5, "trapped": 2.0, "help": 1.2,
            "stranded": 1.8, "rescue": 1.8, "submerged": 1.5}


def synthetic_posts(zones, n=40, seed=1):
    random.seed(seed)
    templates = ["Water rising fast near {z}, need help!", "Street in {z} submerged",
                 "Family trapped on roof in {z}, rescue please", "Light rain at {z}, all fine",
                 "Traffic jam in {z}", "Stranded near bridge {z}"]
    return [{"zone_id": random.choice(zones), "text": random.choice(templates)} for _ in range(n)]


def score_post(text: str) -> float:
    t = text.lower()
    return sum(w for k, w in KEYWORDS.items() if re.search(r"\b" + k + r"\b", t))


def aggregate(posts):
    agg = {}
    for p in posts:
        s = score_post(p["text"].replace("{z}", p["zone_id"]))
        if s > 0:
            agg[p["zone_id"]] = agg.get(p["zone_id"], 0) + s
    return dict(sorted(agg.items(), key=lambda kv: -kv[1]))
