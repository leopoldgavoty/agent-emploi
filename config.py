"""Configuration globale de l'agent de recherche d'emploi Supply Chain - Annecy."""

import os
from pathlib import Path

# Chemins de base
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "jobs.db"
EXCEL_PATH = DATA_DIR / "offres_supply_chain_annecy.xlsx"
CSV_PATH = DATA_DIR / "offres_supply_chain_annecy.csv"

# Paramètres géographiques
LOCATION = {
    "city": "Annecy",
    "postal_code": "74000",
    "department": "74",
    "insee_code": "74010",
    "latitude": 45.8992,
    "longitude": 6.1294,
    "radius_km": 25,  # Bassin du Grand Annecy et alentours (Rumilly, Epagny, Chavanod, Thônes, Argonay)
}

# Profils recherchés & Mots-clés
KEYWORDS_GLOBAL = [
    "supply chain",
    "logistique",
    "approvisionneur",
    "approvisionnements",
    "planificateur",
    "ordonnancement",
    "gestionnaire de stock",
    "coordinateur flux",
    "responsable supply chain",
    "directeur supply chain",
]

# Classification des profils
CATEGORIES = {
    "Direction & Management": [
        "directeur supply chain",
        "responsable supply chain",
        "supply chain manager",
        "directeur logistique",
        "responsable logistique",
        "responsable des flux",
        "responsable approvisionnement",
        "head of supply chain",
    ],
    "Planification & Approvisionnements": [
        "planificateur",
        "approvisionneur",
        "gestionnaire approvisionnement",
        "chargé d'ordonnancement",
        "planificateur de production",
        "demand planner",
        "supply planner",
    ],
    "Opérations & Flux": [
        "coordinateur supply chain",
        "gestionnaire de stock",
        "coordinateur logistique",
        "gestionnaire adv",
        "administration des ventes",
        "affréteur",
        "superviseur logistique",
    ],
    "Achats & Ingénierie": [
        "acheteur supply chain",
        "ingénieur supply chain",
        "consultant supply chain",
        "chef de projet logistique",
    ],
}

# Codes ROME France Travail pour le secteur logistique & supply chain
ROME_CODES = [
    "N1301",  # Conception et organisation de la chaîne logistique
    "N1302",  # Direction de site logistique
    "N1303",  # Intervention technique d'exploitation logistique
    "N1401",  # Direction des transports
    "M1101",  # Achats
    "M1102",  # Direction des achats
]

# Types de contrats prioritaires
CONTRACT_TYPES = ["CDI", "CDD", "Freelance", "Alternance"]

# Statuts de suivi des candidatures
STATUS_OPTIONS = [
    "Nouvelle",
    "À postuler",
    "Candidature envoyée",
    "Archivé",
]
