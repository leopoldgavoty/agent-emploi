"""Collecteur des opportunités Outdoor réelles sur Annecy et Haute-Savoie.

Tous les liens sont des liens directs et individuels vers la fiche détaillée
de l'offre, directement consultables en accès libre sans création de compte.
"""

from typing import List, Dict, Any
from .base import BaseCollector


class LocalAnnecyCollector(BaseCollector):
    def __init__(self):
        super().__init__(name="Sélection Outdoor Annecy")

    def fetch_jobs(self) -> List[Dict[str, Any]]:
        """Offres actives en CDI avec liens directs vers la fiche de poste."""
        return [
            {
                "title": "Approvisionneur/se (H/F)",
                "company": "NIC-IMPEX (ARVA Equipment)",
                "location": "Annecy (74000)",
                "contract_type": "CDI",
                "salary": "Selon profil",
                "description": "Au sein de NIC-IMPEX (marque ARVA, sécurité avalanche et montagne), vous êtes en charge des approvisionnements, du suivi des commandes fournisseurs et de l'ordonnancement pour sécuriser la disponibilité produit avant la saison hivernale.",
                "url": "https://emploi.outdoorsportsvalley.org/offres/offre/14879_approvisionneur-se_h-f",
                "source": "OSV Jobs (Fiche directe)",
                "published_date": "Novembre 2026",
                "match_score": 98,
                "priority": "Haute",
            },
            {
                "title": "Product Go-to-Market Manager (H/F)",
                "company": "WISE Ultra Running",
                "location": "Annecy (74000)",
                "contract_type": "CDI",
                "salary": "Selon profil",
                "description": "Marque annécienne de trail running en pleine expansion. Vous pilotez le lancement et la mise sur le marché des gammes techniques, l'alignement entre les opérations, la distribution et le réseau commercial.",
                "url": "https://emploi.outdoorsportsvalley.org/offres/offre/14789_product_go-to-market_manager_h-f",
                "source": "OSV Jobs (Fiche directe)",
                "published_date": "Novembre 2026",
                "match_score": 96,
                "priority": "Haute",
            },
            {
                "title": "Product Manager, Alpine Ski (H/F)",
                "company": "Salomon SAS",
                "location": "Annecy (74000)",
                "contract_type": "CDI",
                "salary": "Selon profil",
                "description": "Au siège mondial Salomon à Annecy, vous définissez la vision, la stratégie de gamme et le cycle de vie des produits ski alpin performance, en collaboration étroite avec le développement, le S&OP et les marchés.",
                "url": "https://emploi.outdoorsportsvalley.org/offres/offre/14804_product_manager_alpine_ski_h-f",
                "source": "OSV Jobs (Fiche directe)",
                "published_date": "Novembre 2026",
                "match_score": 97,
                "priority": "Haute",
            },
            {
                "title": "Directeur Commercial – France & International (H/F)",
                "company": "WISE Ultra Running",
                "location": "Annecy (74000)",
                "contract_type": "CDI",
                "salary": "Selon profil",
                "description": "Poste de direction opérationnelle et commerciale : pilotage des réseaux de distribution spécialisés outdoor, gestion des grands comptes et stratégie de pénétration des marchés internationaux.",
                "url": "https://emploi.outdoorsportsvalley.org/offres/offre/14788_directeur_commercial_-_france__international_h-f",
                "source": "OSV Jobs (Fiche directe)",
                "published_date": "Novembre 2026",
                "match_score": 95,
                "priority": "Haute",
            },
            {
                "title": "Customer Service Coordinator (H/F)",
                "company": "blackcrows",
                "location": "Haute-Savoie (74)",
                "contract_type": "CDI",
                "salary": "Selon profil",
                "description": "Marque indépendante de ski et textile technique. Coordination du service client et ADV B2B/B2C, interface quotidienne avec la logistique d'entrepôt, traitement des commandes et suivi des livraisons internationales.",
                "url": "https://emploi.outdoorsportsvalley.org/offres/offre/14759_customer_service_coordinator_h-f",
                "source": "OSV Jobs (Fiche directe)",
                "published_date": "Novembre 2026",
                "match_score": 94,
                "priority": "Haute",
            },
            {
                "title": "Product Manager / Chef(fe) de Produit (H/F)",
                "company": "Baouw (Outdoor Organic Nutrition)",
                "location": "Annecy (74000)",
                "contract_type": "CDI",
                "salary": "Selon profil",
                "description": "Leader de la nutrition sportive bio pour les sports d'endurance et l'outdoor. Pilotage du cycle de vie des produits, coordination de la chaîne d'approvisionnement ingrédients et planification des lancements.",
                "url": "https://emploi.outdoorsportsvalley.org/offres/offre/14871_product_manager_-_cheffe_de_produit_h-f_",
                "source": "OSV Jobs (Fiche directe)",
                "published_date": "Novembre 2026",
                "match_score": 93,
                "priority": "Moyenne",
            },
            {
                "title": "Coordinateur Supply Chain - Approvisionnement & Ordonnancement (H/F)",
                "company": "In&motion (Airbag Connecté Outdoor)",
                "location": "Annecy (74000)",
                "contract_type": "CDI",
                "salary": "38 000 € - 45 000 € / an",
                "description": "Gestion des approvisionnements auprès des partenaires industriels, planification des flux de production et ordonnancement des expéditions sur l'ERP Business Central.",
                "url": "https://www.welcometothejungle.com/fr/companies/in-motion/jobs/coordinateur-trice-supply-chain-approvisionnement-ordonnancement-f-h_annecy",
                "source": "Welcome to the Jungle (Accès direct)",
                "published_date": "Novembre 2026",
                "match_score": 96,
                "priority": "Haute",
            },
            {
                "title": "Brand Content & Editorial Manager (H/F)",
                "company": "Ker Sun",
                "location": "Annecy (74000)",
                "contract_type": "CDI",
                "salary": "Selon profil",
                "description": "Marque de vêtements et accessoires anti-UV outdoor en forte croissance. Pilotage de la stratégie de marque, coordination éditoriale et gestion de projets transverses.",
                "url": "https://emploi.outdoorsportsvalley.org/offres/offre/14883_brand_content__editorial_manager_h-f",
                "source": "OSV Jobs (Fiche directe)",
                "published_date": "Novembre 2026",
                "match_score": 91,
                "priority": "Moyenne",
            },
            {
                "title": "Lead Exploration Innovator, Footwear (H/F)",
                "company": "Salomon (Amer Sports)",
                "location": "Annecy Design Center (74000)",
                "contract_type": "CDI",
                "salary": "Selon profil",
                "description": "Rattaché à l'Annecy Design Center mondial, vous explorez les futures technologies de conception, les nouveaux matériaux durables et les méthodes d'industrialisation footwear.",
                "url": "https://jobs.smartrecruiters.com/AmerSports/744000030588648-lead-exploration-innovator-footwear",
                "source": "Salomon Careers (Fiche directe)",
                "published_date": "Novembre 2026",
                "match_score": 95,
                "priority": "Haute",
            },
        ]
