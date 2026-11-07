"""Gestion de la base de données SQLite locale avec dédoublonnage et exports Excel/CSV."""

import sqlite3
import hashlib
import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
import pandas as pd

from config import DB_PATH, EXCEL_PATH, CSV_PATH, CATEGORIES


def compute_job_hash(title: str, company: str, location: str) -> str:
    """Calcule une clé unique pour dédoublonner les offres."""
    raw = f"{title.strip().lower()}|{company.strip().lower()}|{location.strip().lower()}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def categorize_title(title: str) -> str:
    """Catégorise automatiquement l'offre selon son intitulé."""
    title_lower = title.lower()
    for category, keywords in CATEGORIES.items():
        if any(kw in title_lower for kw in keywords):
            return category
    return "Supply Chain & Opérations Outdoor"


class JobDatabase:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        """Initialise le schéma de la base de données."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS jobs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_hash TEXT UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    company TEXT NOT NULL,
                    location TEXT NOT NULL,
                    contract_type TEXT,
                    salary TEXT,
                    description TEXT,
                    url TEXT,
                    source TEXT,
                    category TEXT,
                    published_date TEXT,
                    status TEXT DEFAULT 'Nouvelle',
                    priority TEXT DEFAULT 'Moyenne',
                    notes TEXT DEFAULT '',
                    match_score INTEGER DEFAULT 80,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_job_hash ON jobs(job_hash)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_status ON jobs(status)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_category ON jobs(category)")
            conn.commit()

    def insert_or_update(self, job: Dict[str, Any]) -> bool:
        """Insère une offre ou ignore si déjà existante (dédoublonnage).

        Retourne True si c'est une nouvelle offre insérée, False sinon.
        """
        title = job.get("title", "Offre sans titre").strip()
        company = job.get("company", "Entreprise confidentielle").strip()
        location = job.get("location", "Annecy (74)").strip()
        job_hash = job.get("job_hash") or compute_job_hash(title, company, location)
        category = job.get("category") or categorize_title(title)

        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with self._get_connection() as conn:
            cursor = conn.cursor()
            # Vérifier si l'offre existe déjà
            cursor.execute("SELECT id, status, notes FROM jobs WHERE job_hash = ?", (job_hash,))
            existing = cursor.fetchone()

            if existing:
                # Mise à jour des informations fraîches sans écraser le statut utilisateur
                cursor.execute("""
                    UPDATE jobs SET
                        contract_type = COALESCE(?, contract_type),
                        salary = COALESCE(?, salary),
                        description = COALESCE(?, description),
                        url = COALESCE(?, url),
                        updated_at = ?
                    WHERE job_hash = ?
                """, (
                    job.get("contract_type"),
                    job.get("salary"),
                    job.get("description"),
                    job.get("url"),
                    now,
                    job_hash
                ))
                conn.commit()
                return False
            else:
                cursor.execute("""
                    INSERT INTO jobs (
                        job_hash, title, company, location, contract_type,
                        salary, description, url, source, category,
                        published_date, status, priority, notes, match_score,
                        created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    job_hash,
                    title,
                    company,
                    location,
                    job.get("contract_type", "CDI"),
                    job.get("salary", "Non précisé"),
                    job.get("description", ""),
                    job.get("url", ""),
                    job.get("source", "Veille Annecy"),
                    category,
                    job.get("published_date", datetime.date.today().isoformat()),
                    job.get("status", "Nouvelle"),
                    job.get("priority", "Moyenne"),
                    job.get("notes", ""),
                    job.get("match_score", 85),
                    now,
                    now,
                ))
                conn.commit()
                return True

    def get_all_jobs(self, search: Optional[str] = None, category: Optional[str] = None,
                     status: Optional[str] = None, contract: Optional[str] = None) -> List[Dict[str, Any]]:
        """Récupère les offres selon différents filtres."""
        query = "SELECT * FROM jobs WHERE 1=1"
        params = []

        if search:
            query += " AND (title LIKE ? OR company LIKE ? OR description LIKE ?)"
            term = f"%{search}%"
            params.extend([term, term, term])

        if category and category != "Toutes":
            query += " AND category = ?"
            params.append(category)

        if status and status != "Tous":
            query += " AND status = ?"
            params.append(status)

        if contract and contract != "Tous":
            query += " AND contract_type = ?"
            params.append(contract)

        query += " ORDER BY id DESC"

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def update_status(self, job_id: int, new_status: str, notes: Optional[str] = None, priority: Optional[str] = None):
        """Met à jour le statut, les notes ou la priorité d'une offre."""
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if notes is not None and priority is not None:
                cursor.execute(
                    "UPDATE jobs SET status = ?, notes = ?, priority = ?, updated_at = ? WHERE id = ?",
                    (new_status, notes, priority, now, job_id)
                )
            elif notes is not None:
                cursor.execute(
                    "UPDATE jobs SET status = ?, notes = ?, updated_at = ? WHERE id = ?",
                    (new_status, notes, now, job_id)
                )
            else:
                cursor.execute(
                    "UPDATE jobs SET status = ?, updated_at = ? WHERE id = ?",
                    (new_status, now, job_id)
                )
            conn.commit()

    def get_statistics(self) -> Dict[str, Any]:
        """Calcule les statistiques clés pour le tableau de bord."""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM jobs")
            total_jobs = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM jobs WHERE status = 'Nouvelle'")
            new_jobs = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM jobs WHERE status = 'À postuler'")
            to_apply = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM jobs WHERE status = 'Candidature envoyée'")
            applied = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM jobs WHERE status = 'Archivé'")
            archived = cursor.fetchone()[0]

            cursor.execute("SELECT category, COUNT(*) FROM jobs GROUP BY category")
            by_category = dict(cursor.fetchall())

            cursor.execute("SELECT status, COUNT(*) FROM jobs GROUP BY status")
            by_status = dict(cursor.fetchall())

            cursor.execute("SELECT contract_type, COUNT(*) FROM jobs GROUP BY contract_type")
            by_contract = dict(cursor.fetchall())

            return {
                "total": total_jobs,
                "new": new_jobs,
                "to_apply": to_apply,
                "applied": applied,
                "archived": archived,
                "in_progress": to_apply + applied,
                "by_category": by_category,
                "by_status": by_status,
                "by_contract": by_contract,
            }

    def export_to_excel(self, file_path: Path = EXCEL_PATH) -> Path:
        """Exporte l'ensemble des offres dans un tableur Excel bien formaté."""
        jobs = self.get_all_jobs()
        if not jobs:
            df = pd.DataFrame(columns=[
                "ID", "Titre", "Entreprise", "Lieu", "Contrat", "Salaire",
                "Catégorie", "Statut", "Priorité", "Notes", "Source", "Lien", "Date ajout"
            ])
        else:
            df = pd.DataFrame(jobs)
            cols_map = {
                "id": "ID",
                "title": "Titre",
                "company": "Entreprise",
                "location": "Lieu",
                "contract_type": "Contrat",
                "salary": "Salaire",
                "category": "Catégorie",
                "status": "Statut",
                "priority": "Priorité",
                "notes": "Notes",
                "source": "Source",
                "url": "Lien de l'offre",
                "created_at": "Date d'ajout",
            }
            available_cols = [c for c in cols_map.keys() if c in df.columns]
            df = df[available_cols].rename(columns=cols_map)

        file_path.parent.mkdir(parents=True, exist_ok=True)
        with pd.ExcelWriter(str(file_path), engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Offres Supply Chain Annecy")

        return file_path

    def export_to_csv(self, file_path: Path = CSV_PATH) -> Path:
        """Exporte les offres au format CSV standard UTF-8."""
        jobs = self.get_all_jobs()
        df = pd.DataFrame(jobs) if jobs else pd.DataFrame()
        file_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(str(file_path), index=False, encoding="utf-8-sig", sep=";")
        return file_path
