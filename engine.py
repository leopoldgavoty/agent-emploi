"""Moteur de collecte et d'agrégation des offres d'emploi Supply Chain."""

from typing import Dict, Any, List
from database import JobDatabase
from collectors import FranceTravailCollector, RSSJobCollector, LocalAnnecyCollector
from config import EXCEL_PATH, CSV_PATH


class JobScoutEngine:
    def __init__(self, db: JobDatabase = None):
        self.db = db or JobDatabase()
        self.collectors = [
            FranceTravailCollector(),
            RSSJobCollector(),
            LocalAnnecyCollector(),
        ]

    def run_sync(self) -> Dict[str, Any]:
        """Lance la synchronisation complète de tous les collecteurs.

        Dédoublonne automatiquement les offres, les enregistre dans SQLite,
        et régénère les exports Excel et CSV à jour.
        """
        total_collected = 0
        new_jobs_count = 0
        details = []

        for collector in self.collectors:
            try:
                jobs = collector.fetch_jobs()
                collector_new = 0
                for job in jobs:
                    total_collected += 1
                    is_new = self.db.insert_or_update(job)
                    if is_new:
                        collector_new += 1
                        new_jobs_count += 1
                details.append({
                    "collector": collector.name,
                    "total": len(jobs),
                    "new": collector_new,
                })
            except Exception as e:
                details.append({
                    "collector": collector.name,
                    "error": str(e),
                })

        # Régénération automatique des fichiers Excel et CSV
        excel_file = self.db.export_to_excel(EXCEL_PATH)
        csv_file = self.db.export_to_csv(CSV_PATH)

        return {
            "total_collected": total_collected,
            "new_jobs_count": new_jobs_count,
            "excel_path": str(excel_file),
            "csv_path": str(csv_file),
            "details": details,
        }
