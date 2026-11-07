"""Configuration globale de l'agent Outdoor Job Board - Annecy."""

import os
from pathlib import Path

# Chemins de base
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "jobs.db"
EXCEL_PATH = DATA_DIR / "offres_supply_chain_annecy.xlsx"
CSV_PATH = DATA_DIR / "offres_supply_chain_annecy.csv"

# Paramètres géographiques : Annecy et son écosystème outdoor
LOCATION = {
    "city": "Annecy",
    "postal_code": "74000",
    "department": "74",
    "insee_code": "74010",
    "latitude": 45.8992,
    "longitude": 6.1294,
    "radius_km": 30,  # Grand Annecy, Metz-Tessy, Epagny, Chavanod, Thônes, Rumilly
}

# Marques et entreprises phares de l'industrie outdoor ciblées
OUTDOOR_BRANDS = [
    "Salomon",
    "Millet",
    "WISE",
    "Samaya",
    "Arva",
    "Cairn",
    "Scott Sports",
    "Décathlon",
    "Arc'teryx",
    "Amer Sports",
    "Snowleader",
    "Hardloop",
    "Fusalp",
    "TSL Outdoor",
    "Baouw",
    "In&motion",
    "Outdoor Sports Valley",
    "Eider",
    "Picture Organic",
]

# Mots-clés de veille (Supply Chain, Planning, Opérations, ADV, Service Client)
KEYWORDS_GLOBAL = [
    "supply chain",
    "demand planning",
    "supply planning",
    "distribution planning",
    "s&op",
    "planificateur",
    "approvisionneur",
    "approvisionnement",
    "logistique",
    "operations",
    "opérations",
    "service client",
    "customer service",
    "adv",
    "administration des ventes",
    "gestionnaire de stock",
    "ordonnancement",
    "outdoor",
]

# Classification des métiers Supply Chain & Opérations Outdoor
CATEGORIES = {
    "Demand & Supply Planning / S&OP": [
        "demand planning",
        "supply planning",
        "distribution planning",
        "s&op",
        "planificateur",
        "demand planner",
        "supply planner",
        "planification",
        "forecasting",
        "prévisions",
        "ordonnancement",
    ],
    "Direction & Management Opérations": [
        "directeur supply chain",
        "responsable supply chain",
        "supply chain manager",
        "head of operations",
        "directeur des opérations",
        "responsable opérations",
        "directeur logistique",
        "responsable logistique",
        "operations manager",
    ],
    "Approvisionnements & Achats": [
        "approvisionneur",
        "gestionnaire approvisionnement",
        "chargé d'approvisionnement",
        "acheteur supply",
        "sourcing",
        "acheteur outdoor",
    ],
    "Logistique & Distribution": [
        "gestionnaire de stock",
        "coordinateur logistique",
        "responsable entrepôt",
        "affréteur",
        "distribution",
        "flux physiques",
    ],
    "Service Client & ADV (Customer Operations)": [
        "service client",
        "customer service",
        "adv",
        "administration des ventes",
        "customer care",
        "chargé de clientèle",
        "order to cash",
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

# Type de contrat : CDI UNIQUEMENT selon vos critères
CONTRACT_TYPES = ["CDI"]

# Statuts de qualification et suivi
STATUS_OPTIONS = [
    "Nouvelle",
    "À postuler",
    "Candidature envoyée",
    "Archivé",
]
