"""Interface en ligne de commande pour lancer la collecte ou exporter les données."""

import argparse
from engine import JobScoutEngine
from database import JobDatabase


def main():
    parser = argparse.ArgumentParser(description="Agent de veille Emploi Supply Chain - Annecy")
    parser.add_argument("--sync", action="store_true", help="Lancer la recherche et synchroniser toutes les sources")
    parser.add_argument("--export", action="store_true", help="Générer les fichiers Excel et CSV à jour")
    parser.add_argument("--stats", action="store_true", help="Afficher les statistiques actuelles de la base")
    parser.add_argument("--list", action="store_true", help="Lister les offres actives")

    args = parser.parse_args()
    db = JobDatabase()
    engine = JobScoutEngine(db)

    if args.sync or (not args.export and not args.stats and not args.list):
        print("🔍 Lancement de la synchronisation des offres Supply Chain sur Annecy...")
        res = engine.run_sync()
        print(f"✅ Synchronisation terminée !")
        print(f"📦 Total offres traitées : {res['total_collected']}")
        print(f"✨ Nouvelles offres ajoutées : {res['new_jobs_count']}")
        print(f"📊 Fichier Excel : {res['excel_path']}")
        print(f"📄 Fichier CSV   : {res['csv_path']}")
        return

    if args.stats:
        stats = db.get_statistics()
        print("=" * 40)
        print("📊 STATISTIQUES DU BASSIN D'ANNECY")
        print("=" * 40)
        print(f"Total offres : {stats['total']}")
        print(f"Nouvelles    : {stats['new']}")
        print(f"En cours     : {stats['in_progress']}")
        print("\nPar catégorie :")
        for cat, count in stats["by_category"].items():
            print(f"  • {cat}: {count}")
        return

    if args.export:
        excel_path = db.export_to_excel()
        csv_path = db.export_to_csv()
        print(f"✅ Exports générés avec succès :")
        print(f"  Excel: {excel_path}")
        print(f"  CSV:   {csv_path}")
        return

    if args.list:
        jobs = db.get_all_jobs()
        print(f"\n📋 Liste des {len(jobs)} offres enregistrées :")
        for j in jobs:
            print(f"[{j['id']}] {j['title']} | {j['company']} ({j['location']}) - {j['contract_type']} - Statut: {j['status']}")


if __name__ == "__main__":
    main()
