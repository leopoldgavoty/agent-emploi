"""Collecteur officiel pour l'API France Travail (ex Pôle Emploi)."""

import os
import requests
from typing import List, Dict, Any, Optional
from .base import BaseCollector
from config import LOCATION, ROME_CODES


class FranceTravailCollector(BaseCollector):
    AUTH_URL = "https://entreprise.francetravail.fr/connexion/oauth2/access_token?realm=%2Fpartenaire"
    SEARCH_URL = "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search"

    def __init__(self, client_id: Optional[str] = None, client_secret: Optional[str] = None):
        super().__init__(name="France Travail")
        self.client_id = client_id or os.getenv("FRANCE_TRAVAIL_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("FRANCE_TRAVAIL_CLIENT_SECRET")
        self.access_token = None

    def _authenticate(self) -> bool:
        """Obtient un jeton OAuth2 auprès des serveurs France Travail."""
        if not self.client_id or not self.client_secret:
            return False

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": "api_offresdemploiv2 o2dsoffre",
        }
        try:
            resp = requests.post(self.AUTH_URL, data=data, headers=headers, timeout=10)
            if resp.status_code == 200:
                self.access_token = resp.json().get("access_token")
                return True
        except Exception as e:
            print(f"[FranceTravailCollector] Erreur d'authentification: {e}")
        return False

    def fetch_jobs(self) -> List[Dict[str, Any]]:
        """Interroge l'API des offres d'emploi pour Annecy et sa périphérie."""
        if not self._authenticate():
            print("[FranceTravailCollector] Clés d'API non configurées ou invalides. Mode passif.")
            return []

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/json",
        }

        jobs = []
        keywords = [
            "supply chain outdoor",
            "demand planner",
            "supply planner",
            "approvisionneur",
            "responsable logistique",
            "adv outdoor",
            "s&op",
        ]

        for kw in keywords:
            params = {
                "motsCles": kw,
                "commune": LOCATION["insee_code"],
                "distance": LOCATION["radius_km"],
                "typeContrat": "CDI",
                "range": "0-49",
            }
            try:
                resp = requests.get(self.SEARCH_URL, headers=headers, params=params, timeout=15)
                if resp.status_code == 200:
                    data = resp.json()
                    for item in data.get("resultats", []):
                        job = self._normalize_item(item)
                        if job:
                            jobs.append(job)
                elif resp.status_code == 206:  # Contenu partiel
                    data = resp.json()
                    for item in data.get("resultats", []):
                        job = self._normalize_item(item)
                        if job:
                            jobs.append(job)
            except Exception as e:
                print(f"[FranceTravailCollector] Erreur lors de la requête pour '{kw}': {e}")

        return jobs

    def _normalize_item(self, item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        try:
            lieu = item.get("lieuTravail", {})
            entreprise = item.get("entreprise", {})
            salaire_info = item.get("salaire", {})

            return {
                "title": item.get("intitule", "Offre Supply Chain"),
                "company": entreprise.get("nom", "Confidentiel / Cabinet"),
                "location": lieu.get("libelle", "Annecy (74)"),
                "contract_type": item.get("typeContratLibelle", item.get("typeContrat", "CDI")),
                "salary": salaire_info.get("libelle", "Non précisé"),
                "description": item.get("description", "")[:1000],
                "url": item.get("origineOffre", {}).get("urlOrigine", f"https://candidat.francetravail.fr/offres/recherche/detail/{item.get('id')}"),
                "source": "France Travail API",
                "published_date": item.get("dateCreation", "")[:10],
            }
        except Exception:
            return None
