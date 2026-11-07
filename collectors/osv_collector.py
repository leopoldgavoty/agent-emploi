"""Collecteur officiel en direct depuis la plateforme OSV Jobs (Outdoor Sports Valley).

Extrait directement les annonces réelles avec leur lien direct individuel :
https://emploi.outdoorsportsvalley.org/offres/offre/<id>_<titre>
"""

import urllib.request
from bs4 import BeautifulSoup
from typing import List, Dict, Any
from .base import BaseCollector


class OSVCollector(BaseCollector):
    def __init__(self):
        super().__init__(name="OSV Jobs Direct")
        self.base_url = "https://emploi.outdoorsportsvalley.org/offres/?pge="

    def fetch_jobs(self) -> List[Dict[str, Any]]:
        jobs = []
        for pge in range(1, 12):
            url = f"{self.base_url}{pge}"
            try:
                req = urllib.request.Request(
                    url,
                    headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
                )
                html = urllib.request.urlopen(req, timeout=12).read()
                soup = BeautifulSoup(html, "html.parser")
                cards = soup.find_all("a", class_="group")
                if not cards:
                    break

                for a in cards:
                    title_tag = a.find("h1")
                    if not title_tag:
                        continue
                    title = title_tag.get_text(strip=True)

                    ent_tag = a.find("p", class_="entreprise")
                    company = ent_tag.get_text(strip=True).split("/")[0].strip() if ent_tag else "Entreprise OSV"

                    poste_tag = a.find("p", class_="poste")
                    details_text = poste_tag.get_text(strip=True) if poste_tag else ""

                    href = a.get("href", "")
                    if href.startswith("http://"):
                        href = href.replace("http://", "https://")

                    desc_tag = a.find("p", class_="mt-2")
                    desc = desc_tag.get_text(strip=True) if desc_tag else ""

                    det_lower = details_text.lower()
                    title_lower = title.lower()

                    # On filtre strictement sur CDI
                    is_cdi = "cdi" in det_lower or "cdi" in title_lower
                    # On cible Annecy et l'écosystème alpin
                    is_local = any(loc in det_lower for loc in ["annecy", "74", "haute-savoie", "chamonix", "passy", "epagny", "pringy", "saint-jorioz", "alpes"])

                    if is_cdi and is_local and "/offre/" in href:
                        location = "Annecy (74)"
                        if "chamonix" in det_lower:
                            location = "Chamonix (74)"
                        elif "passy" in det_lower:
                            location = "Passy (74)"
                        elif "epagny" in det_lower:
                            location = "Epagny Metz-Tessy (74)"

                        jobs.append({
                            "title": title,
                            "company": company,
                            "location": location,
                            "contract_type": "CDI",
                            "salary": "Selon profil",
                            "description": desc or f"Poste en CDI actuellement ouvert chez {company} via la plateforme Outdoor Sports Valley.",
                            "url": href,
                            "source": "OSV Jobs",
                            "published_date": "Novembre 2026",
                        })
            except Exception as e:
                break

        return jobs
