"""Application Web Streamlit - Dashboard de Suivi des Offres Supply Chain à Annecy."""

import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path

from config import (
    LOCATION, CATEGORIES, CONTRACT_TYPES, STATUS_OPTIONS,
    EXCEL_PATH, CSV_PATH
)
from database import JobDatabase
from engine import JobScoutEngine

# Configuration de la page
st.set_page_config(
    page_title="Supply Chain Jobs Annecy | Agent de Veille",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialisation de la base et du moteur
@st.cache_resource
def get_db():
    db = JobDatabase()
    # Initialisation au premier lancement si la base est vide
    stats = db.get_statistics()
    if stats["total"] == 0:
        engine = JobScoutEngine(db)
        engine.run_sync()
    return db

db = get_db()

# Custom CSS pour une interface soignée et moderne
st.markdown("""
<style>
    .metric-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .job-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
        transition: all 0.2s ease;
    }
    .job-card:hover {
        border-color: #3b82f6;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.08);
    }
    .tag {
        display: inline-block;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 500;
        margin-right: 6px;
    }
    .tag-cdi { background: #dcfce7; color: #166534; }
    .tag-loc { background: #e0f2fe; color: #0369a1; }
    .tag-cat { background: #f3e8ff; color: #6b21a8; }
    .tag-salary { background: #fef9c3; color: #854d0e; }
</style>
""", unsafe_allow_html=True)

# Barre latérale : Synchronisation et Filtres
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?w=400&q=80", use_container_width=True)
    st.title("📦 Agent Supply Chain")
    st.caption(f"📍 Bassin d'Annecy ({LOCATION['department']}) • Rayon {LOCATION['radius_km']} km")

    st.markdown("---")
    st.subheader("⚡ Action Rapide")

    if st.button("🔄 Lancer la recherche maintenant", use_container_width=True, type="primary"):
        with st.spinner("Interrogation des sources d'offres en cours..."):
            engine = JobScoutEngine(db)
            res = engine.run_sync()
            st.success(f"Synchronisation terminée ! {res['new_jobs_count']} nouvelle(s) offre(s) détectée(s).")
            st.rerun()

    st.markdown("---")
    st.subheader("🔍 Filtres de Recherche")

    search_query = st.text_input("Mots-clés (poste, entreprise, compétence)", placeholder="ex: Directeur, Salomon, ERP...")

    category_filter = st.selectbox(
        "Catégorie métier",
        ["Toutes"] + list(CATEGORIES.keys()) + ["Autre Supply Chain"],
    )

    status_filter = st.selectbox(
        "Statut de candidature",
        ["Tous"] + STATUS_OPTIONS,
    )

    contract_filter = st.selectbox(
        "Type de contrat",
        ["Tous"] + CONTRACT_TYPES,
    )

    st.markdown("---")
    st.subheader("📥 Export des données")

    # Boutons d'export direct Excel / CSV
    if EXCEL_PATH.exists():
        with open(EXCEL_PATH, "rb") as f:
            st.download_button(
                label="📊 Télécharger Excel (.xlsx)",
                data=f.read(),
                file_name=f"offres_supply_chain_annecy_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )

    if CSV_PATH.exists():
        with open(CSV_PATH, "rb") as f:
            st.download_button(
                label="📄 Télécharger CSV (.csv)",
                data=f.read(),
                file_name=f"offres_supply_chain_annecy_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True,
            )

# En-tête principal & KPIs
stats = db.get_statistics()

st.title("🚀 Veille & Suivi des Offres Supply Chain — Annecy")
st.markdown("Agent automatisé de détection, dédoublonnage et gestion des candidatures en Haute-Savoie.")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Offres Détectées", stats["total"])
with col2:
    st.metric("Nouvelles Offres", stats["new"], delta=f"{stats['new']} à traiter")
with col3:
    st.metric("Candidatures Actives", stats["in_progress"])
with col4:
    postes_cadres = stats["by_category"].get("Direction & Management", 0)
    st.metric("Postes Cadres / Management", postes_cadres)

st.markdown("<br>", unsafe_allow_html=True)

# Onglets principaux
tab1, tab2, tab3 = st.tabs(["📋 Liste des Opportunités", "📌 Suivi Kanban", "📈 Analyse du Marché"])

# Récupération des données filtrées
jobs = db.get_all_jobs(
    search=search_query,
    category=category_filter,
    status=status_filter,
    contract=contract_filter,
)

with tab1:
    st.subheader(f"Offres correspondantes ({len(jobs)})")

    if not jobs:
        st.info("Aucune offre ne correspond à vos filtres actuels. Réinitialisez les filtres ou lancez une synchronisation.")
    else:
        for job in jobs:
            with st.container():
                st.markdown(f"""
                <div class="job-card">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div>
                            <h3 style="margin: 0 0 6px 0; color: #1e293b; font-size: 1.15rem;">
                                {job['title']}
                            </h3>
                            <p style="margin: 0 0 10px 0; color: #475569; font-weight: 500;">
                                🏢 <b>{job['company']}</b> &nbsp;•&nbsp; 📍 {job['location']} &nbsp;•&nbsp; 📅 {job['published_date']}
                            </p>
                        </div>
                        <div style="text-align: right;">
                            <span class="tag tag-cdi">{job['contract_type']}</span>
                            <span class="tag tag-salary">{job['salary']}</span>
                        </div>
                    </div>
                    <div style="margin: 8px 0;">
                        <span class="tag tag-cat">🏷️ {job['category']}</span>
                        <span class="tag tag-loc">Source : {job['source']}</span>
                    </div>
                    <p style="color: #334155; font-size: 0.92rem; line-height: 1.5; margin: 12px 0;">
                        {job['description']}
                    </p>
                </div>
                """, unsafe_allow_html=True)

                # Actions et changement de statut sous chaque carte
                c_act1, c_act2, c_act3 = st.columns([2, 3, 2])
                with c_act1:
                    new_st = st.selectbox(
                        "Statut",
                        STATUS_OPTIONS,
                        index=STATUS_OPTIONS.index(job["status"]) if job["status"] in STATUS_OPTIONS else 0,
                        key=f"status_{job['id']}",
                    )
                    if new_st != job["status"]:
                        db.update_status(job["id"], new_st)
                        st.toast(f"Statut mis à jour : {new_st}")
                        st.rerun()

                with c_act2:
                    user_notes = st.text_input(
                        "Notes personnelles",
                        value=job.get("notes") or "",
                        key=f"notes_{job['id']}",
                        placeholder="ex: Envoyé CV version Cadre, relance le 12/11",
                    )
                    if user_notes != (job.get("notes") or ""):
                        db.update_status(job["id"], job["status"], notes=user_notes)

                with c_act3:
                    st.write("")
                    st.write("")
                    if job.get("url"):
                        st.link_button("🔗 Consulter / Postuler", job["url"], use_container_width=True)

                st.markdown("<hr style='margin: 10px 0 24px 0; border: none; border-top: 1px dashed #cbd5e1;'>", unsafe_allow_html=True)

with tab2:
    st.subheader("Tableau Kanban des Candidatures")
    st.caption("Visualisez et organisez l'état d'avancement de vos démarches pour chaque entreprise d'Annecy.")

    kanban_cols = ["Nouvelle", "À postuler", "Candidature envoyée", "Entretien planifié"]
    k_cols = st.columns(len(kanban_cols))

    all_raw_jobs = db.get_all_jobs()

    for idx, col_name in enumerate(kanban_cols):
        with k_cols[idx]:
            col_jobs = [j for j in all_raw_jobs if j["status"] == col_name]
            st.markdown(f"### {col_name} ({len(col_jobs)})")
            for j in col_jobs:
                with st.expander(f"**{j['title'][:32]}...**\n_{j['company']}_"):
                    st.write(f"**Lieu :** {j['location']}")
                    st.write(f"**Salaire :** {j['salary']}")
                    if j.get("notes"):
                        st.info(f"📝 {j['notes']}")
                    if j.get("url"):
                        st.link_button("Lien offre", j["url"])

with tab3:
    st.subheader("Analyse du Bassin de l'Emploi Supply Chain - Annecy")

    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.markdown("#### Répartition par Catégorie de Poste")
        if stats["by_category"]:
            cat_df = pd.DataFrame(list(stats["by_category"].items()), columns=["Catégorie", "Nombre"])
            st.bar_chart(cat_df.set_index("Catégorie"))

    with col_g2:
        st.markdown("#### État du Pipeline de Candidatures")
        if stats["by_status"]:
            status_df = pd.DataFrame(list(stats["by_status"].items()), columns=["Statut", "Nombre"])
            st.bar_chart(status_df.set_index("Statut"))

    st.markdown("---")
    st.markdown("""
    #### 💡 Analyse du marché local (Grand Annecy & Haute-Savoie)
    * **Forte demande de profils mixtes industrie / international** : Grâce aux grands comptes locaux (outdoor comme Salomon, décolletage et mécanique de précision dans la vallée, agroalimentaire et fabrication de mobilier haut de gamme).
    * **Valorisation des outils modernes** : Les recruteurs recherchent particulièrement la maîtrise d'ERP majeurs (SAP, Microsoft Dynamics Business Central) et des pratiques S&OP / flux tirés Kanban.
    * **Niveau de rémunération attractif** : Proximité suisse et dynamisme industriel conduisent à des packages salariaux généralement supérieurs de 10% à 20% à la moyenne nationale sur les postes Cadres / Management.
    """)
