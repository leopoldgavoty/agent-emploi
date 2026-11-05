# 📦 Agent de Veille Emploi Supply Chain — Annecy (74)

Agent intelligent et tableau de bord automatisé dédié à la recherche, au dédoublonnage et au suivi de candidatures dans le secteur de la **Supply Chain, des Achats et de la Logistique** sur le bassin d'**Annecy et de la Haute-Savoie** (rayon 25 km).

---

## 🎯 Fonctionnalités Clés

- **Agrégation multi-sources** : Collecte des offres issues de France Travail (API v2), Apec, sites carrières d'entreprises locales (outdoor, industrie mécanique, e-commerce) et jobboards.
- **Dédoublonnage intelligent** : Empreinte cryptographique unique pour chaque offre (`titre + entreprise + localisation`) évitant les doublons lors des scans répétés.
- **Stockage SQLite local & Exports automatiques** :
  - Base de données locale `data/jobs.db`.
  - Export **Excel (`.xlsx`)** et **CSV** régénérés automatiquement à chaque nouvelle détection.
- **Interface Web Interactive (Streamlit)** :
  - **Tableau de bord & KPIs** : Offres totales, nouvelles offres, postes cadres/management, répartition par sous-domaine.
  - **Filtres multicritères** : Recherche par mots-clés, catégories (Direction, Approvisionnements, Ordonnancement, ADV), types de contrat (CDI, CDD).
  - **Kanban de suivi des candidatures** : Gestion visuelle du statut (*Nouvelle*, *À postuler*, *Candidature envoyée*, *Entretien*, *Offre reçue*).
  - **Notes personnelles** : Possibilité d'annoter chaque offre (date d'envoi du CV, contact RH, date de relance).

---

## 🚀 Démarrage Rapide

### 1. Prérequis sur macOS
Si les outils de développement ne sont pas encore installés sur votre Mac, ouvrez votre Terminal et lancez :
```bash
xcode-select --install
```
*(ou installez Python 3 depuis [python.org](https://www.python.org/downloads/)).*

### 2. Installation des dépendances
Dans le dossier du projet :
```bash
pip install -r requirements.txt
```

### 3. Lancer le Dashboard Web Streamlit
```bash
streamlit run app.py
```
Le tableau de bord s'ouvrira automatiquement dans votre navigateur à l'adresse `http://localhost:8501`.

### 4. Utilisation en ligne de commande (CLI)
Vous pouvez également synchroniser ou exporter sans lancer l'interface web :
```bash
# Lancer la recherche et synchroniser toutes les sources
python cli.py --sync

# Afficher les statistiques de la veille
python cli.py --stats

# Régénérer les exports Excel et CSV
python cli.py --export

# Lister les offres enregistrées
python cli.py --list
```

---

## 📁 Structure du Projet

```text
agent emploi/
├── app.py                      # Application Web Streamlit (Dashboard & Kanban)
├── cli.py                      # Interface en ligne de commande (script d'automatisation)
├── config.py                   # Configuration géographique (Annecy, 74010) et filtres métiers
├── database.py                 # Gestionnaire SQLite avec dédoublonnage et export Excel/CSV
├── engine.py                   # Moteur d'orchestration des collecteurs
├── requirements.txt            # Dépendances Python
├── .env.example                # Configuration des clés d'API (France Travail, alertes...)
├── collectors/
│   ├── base.py                 # Modèle abstrait de collecteur
│   ├── france_travail.py       # API officielle France Travail (v2)
│   ├── rss_collector.py        # Connecteur de flux RSS (Apec, jobboards)
│   └── local_annecy.py         # Collecteur des opportunités réelles du bassin annécien
└── data/
    ├── jobs.db                 # Base de données locale SQLite
    ├── offres_supply_chain_annecy.xlsx  # Tableur Excel synchronisé
    └── offres_supply_chain_annecy.csv   # Fichier CSV
```

---

## ⚙️ Configuration Avancée (Optionnelle)

### Clés France Travail (ex-Pôle Emploi)
Pour activer l'accès direct aux serveurs France Travail :
1. Créez un compte gratuit sur [francetravail.io](https://francetravail.io).
2. Créez une application avec l'API **"Offres d'emploi v2"**.
3. Créez un fichier `.env` à la racine :
```env
FRANCE_TRAVAIL_CLIENT_ID=votre_client_id
FRANCE_TRAVAIL_CLIENT_SECRET=votre_client_secret
```

---

## ⏰ Automatisation de la Veille Quotidienne

Pour exécuter la recherche automatiquement tous les matins (par exemple à 8h00), vous pouvez configurer une tâche cron sur votre Mac :
```bash
crontab -e
```
Ajoutez la ligne suivante :
```text
0 8 * * * cd "/Users/leopoldgavoty/Desktop/agent emploi" && python3 cli.py --sync >> data/sync.log 2>&1
```
