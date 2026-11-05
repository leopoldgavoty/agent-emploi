"""Collecteur pour les flux RSS publics d'offres d'emploi."""

import feedparser
from typing import List, Dict, Any
from .base import BaseCollector


class RSSJobCollector(BaseCollector):
    def __init__(self):
        super().__init__(name="Flux RSS Emploi")
        # Exemples d'URL de flux RSS spécialisés ou régionaux
        self.feed_urls = [
            "https://www.apec.fr/recherche-emploi.rss?motsCles=supply+chain&lieux=74010",
        ]

    def fetch_jobs(self) -> List[Dict[str, Any]]:
        jobs = []
        for url in self.feed_urls:
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries:
                    title = entry.get("title", "")
                    link = entry.get("link", "")
                    summary = entry.get("summary", "")
                    published = entry.get("published", "")

                    if "annecy" in (title + summary).lower() or "74" in (title + summary):
                        jobs.append({
                            "title": title,
                            "company": "Recruteur Apec / Haute-Savoie",
                            "location": "Annecy et agglomération (74)",
                            "contract_type": "CDI",
                            "salary": "Non précisé",
                            "description": summary[:1000],
                            "url": link,
                            "source": "Apec RSS",
                            "published_date": published[:10] if published else "",
                        })
            except Exception as e:
                print(f"[RSSJobCollector] Impossible de lire le flux {url}: {e}")
        return jobs
