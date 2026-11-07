"""Application Web Streamlit - Outdoor Job Board 🦦"""

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
    page_title="Outdoor Job Board 🦦",
    page_icon="🦦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialisation de la base et du moteur
@st.cache_resource
def get_db():
    db = JobDatabase()
    stats = db.get_statistics()
    if stats["total"] == 0:
        engine = JobScoutEngine(db)
        engine.run_sync()
    return db

db = get_db()

# Custom CSS pour une interface épurée et moderne
st.markdown("""
<style>
    .job-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
        transition: all 0.2s ease;
    }
    .job-card:hover {
        border-color: #0284c7;
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.08);
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
    .tag-status-new { background: #f1f5f9; color: #475569; }
    .tag-status-apply { background: #fef3c7; color: #b45309; }
    .tag-status-sent { background: #dbeafe; color: #1d4ed8; }
    .tag-status-archived { background: #f3f4f6; color: #6b7280; }
</style>
""", unsafe_allow_html=True)

# Barre latérale : Actions et Filtres
with st.sidebar:
    st.subheader("⚡ Action Rapide")

    if st.button("🔄 Lancer la recherche maintenant", use_container_width=True, type="primary"):
        with st.spinner("Recherche d'offres en cours sur le bassin d'Annecy..."):
            engine = JobScoutEngine(db)
            res = engine.run_sync()
            st.success(f"Synchronisation terminée ! {res['new_jobs_count']} nouvelle(s) offre(s) détectée(s).")
            st.rerun()

    st.markdown("---")
    st.subheader("🔍 Filtres de Recherche")

    search_query = st.text_input(
        "Mots-clés (poste, entreprise, compétence)",
        placeholder="ex: Salomon, Directeur, S&OP...",
    )

    category_filter = st.selectbox(
        "Catégorie métier",
        ["Toutes"] + list(CATEGORIES.keys()) + ["Autre Supply Chain"],
    )

    contract_filter = st.selectbox(
        "Type de contrat",
        ["Tous"] + CONTRACT_TYPES,
    )

    st.markdown("---")
    st.subheader("📥 Export des données")

    if EXCEL_PATH.exists():
        with open(EXCEL_PATH, "rb") as f:
            st.download_button(
                label="📊 Télécharger Excel (.xlsx)",
                data=f.read(),
                file_name=f"outdoor_jobs_annecy_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )

    if CSV_PATH.exists():
        with open(CSV_PATH, "rb") as f:
            st.download_button(
                label="📄 Télécharger CSV (.csv)",
                data=f.read(),
                file_name=f"outdoor_jobs_annecy_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True,
            )

# En-tête principal & KPIs
stats = db.get_statistics()

st.title("Outdoor Job Board 🦦")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Offres Détectées", stats["total"])
with col2:
    st.metric("Nouvelles Opportunités", stats["new"], delta=f"{stats['new']} à qualifier")
with col3:
    st.metric("À postuler", stats["to_apply"])
with col4:
    st.metric("Candidatures envoyées", stats["applied"])

st.markdown("<br>", unsafe_allow_html=True)

# Les 3 onglets principaux
tab1, tab2, tab3 = st.tabs(["🎯 Opportunités", "📌 Suivi Kanban", "🗄️ Archivées"])

# ----------------------------------------------------
# ONGLET 1 : Opportunités (Nouvelles offres à qualifier)
# ----------------------------------------------------
with tab1:
    col_filter, col_info = st.columns([1, 2])
    with col_filter:
        status_filter_tab1 = st.selectbox(
            "Filtrer par statut :",
            ["Nouvelles uniquement", "Toutes", "À postuler", "Candidature envoyée", "Archivé"],
            index=0,
            key="tab1_status_filter",
        )

    # Déterminer le statut à interroger
    query_status = None
    if status_filter_tab1 == "Nouvelles uniquement":
        query_status = "Nouvelle"
    elif status_filter_tab1 != "Toutes":
        query_status = status_filter_tab1

    jobs_tab1 = db.get_all_jobs(
        search=search_query,
        category=category_filter,
        status=query_status,
        contract=contract_filter,
    )

    with col_info:
        st.write("")
        st.caption(f"**{len(jobs_tab1)}** offre(s) affichée(s)")

    if not jobs_tab1:
        st.info("🎉 Aucune nouvelle offre en attente de traitement ! Cliquez sur '🔄 Lancer la recherche maintenant' pour scanner de nouveaux postes.")
    else:
        for job in jobs_tab1:
            with st.container():
                st.markdown(f"""
                <div class="job-card">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div>
                            <h3 style="margin: 0 0 6px 0; color: #0f172a; font-size: 1.15rem;">
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

                # Barre d'actions sous chaque offre
                c_stat, c_note, c_link = st.columns([2, 3, 2])
                with c_stat:
                    current_idx = STATUS_OPTIONS.index(job["status"]) if job["status"] in STATUS_OPTIONS else 0
                    new_st = st.selectbox(
                        "Attribuer un statut :",
                        STATUS_OPTIONS,
                        index=current_idx,
                        key=f"tab1_stat_{job['id']}",
                    )
                    if new_st != job["status"]:
                        db.update_status(job["id"], new_st)
                        st.toast(f"Offre déplacée vers : {new_st} !")
                        st.rerun()

                with c_note:
                    user_notes = st.text_input(
                        "Note personnelle :",
                        value=job.get("notes") or "",
                        key=f"tab1_note_{job['id']}",
                        placeholder="ex: Contact RH Salomon, relance le 12/11...",
                    )
                    if user_notes != (job.get("notes") or ""):
                        db.update_status(job["id"], job["status"], notes=user_notes)

                with c_link:
                    st.write("")
                    st.write("")
                    if job.get("url"):
                        st.link_button("🔗 Consulter / Postuler", job["url"], use_container_width=True)

                st.markdown("<hr style='margin: 8px 0 20px 0; border: none; border-top: 1px dashed #cbd5e1;'>", unsafe_allow_html=True)

# ----------------------------------------------------
# ONGLET 2 : Suivi Kanban (À postuler & Candidature envoyée)
# ----------------------------------------------------
with tab2:
    st.subheader("Pipeline des Candidatures")
    st.caption("Suivez vos démarches actives en cours sur le bassin annécien.")

    col_k1, col_k2 = st.columns(2)

    all_jobs = db.get_all_jobs(search=search_query, category=category_filter, contract=contract_filter)
    to_apply_jobs = [j for j in all_jobs if j["status"] == "À postuler"]
    applied_jobs = [j for j in all_jobs if j["status"] == "Candidature envoyée"]

    with col_k1:
        st.markdown(f"### 🎯 À postuler ({len(to_apply_jobs)})")
        if not to_apply_jobs:
            st.info("Aucune offre marquée 'À postuler'. Définissez ce statut depuis l'onglet Opportunités.")
        for j in to_apply_jobs:
            with st.expander(f"**{j['title']}** — {j['company']}", expanded=True):
                st.write(f"📍 **Lieu :** {j['location']} &nbsp;|&nbsp; 💰 **Salaire :** {j['salary']}")
                if j.get("description"):
                    st.caption(j["description"][:250] + "...")
                
                # Notes rapides
                notes_val = st.text_input("Notes :", value=j.get("notes") or "", key=f"k_note_{j['id']}")
                if notes_val != (j.get("notes") or ""):
                    db.update_status(j["id"], j["status"], notes=notes_val)

                # Changement de statut rapide
                c_act1, c_act2, c_act3 = st.columns([1, 1, 1])
                with c_act1:
                    if st.button("✉️ Candidature envoyée", key=f"send_{j['id']}", use_container_width=True):
                        db.update_status(j["id"], "Candidature envoyée")
                        st.rerun()
                with c_act2:
                    if st.button("🗄️ Archiver", key=f"arch_k1_{j['id']}", use_container_width=True):
                        db.update_status(j["id"], "Archivé")
                        st.rerun()
                with c_act3:
                    if j.get("url"):
                        st.link_button("Lien offre ↗", j["url"], use_container_width=True)

    with col_k2:
        st.markdown(f"### ✉️ Candidature envoyée ({len(applied_jobs)})")
        if not applied_jobs:
            st.info("Aucune candidature envoyée pour le moment.")
        for j in applied_jobs:
            with st.expander(f"**{j['title']}** — {j['company']}", expanded=True):
                st.write(f"📍 **Lieu :** {j['location']} &nbsp;|&nbsp; 💰 **Salaire :** {j['salary']}")
                if j.get("description"):
                    st.caption(j["description"][:250] + "...")

                # Notes rapides
                notes_val = st.text_input("Notes de suivi :", value=j.get("notes") or "", key=f"k_app_note_{j['id']}")
                if notes_val != (j.get("notes") or ""):
                    db.update_status(j["id"], j["status"], notes=notes_val)

                # Actions
                c_act1, c_act2, c_act3 = st.columns([1, 1, 1])
                with c_act1:
                    if st.button("↩️ Revenir à postuler", key=f"back_{j['id']}", use_container_width=True):
                        db.update_status(j["id"], "À postuler")
                        st.rerun()
                with c_act2:
                    if st.button("🗄️ Archiver", key=f"arch_k2_{j['id']}", use_container_width=True):
                        db.update_status(j["id"], "Archivé")
                        st.rerun()
                with c_act3:
                    if j.get("url"):
                        st.link_button("Lien offre ↗", j["url"], use_container_width=True)

# ----------------------------------------------------
# ONGLET 3 : Offres Archivées
# ----------------------------------------------------
with tab3:
    st.subheader("Offres Archivées")
    st.caption("Consultez ou restaurez les offres d'emploi que vous avez écartées ou clôturées.")

    archived_jobs = db.get_all_jobs(
        search=search_query,
        category=category_filter,
        status="Archivé",
        contract=contract_filter,
    )

    if not archived_jobs:
        st.info("Aucune offre archivée pour l'instant.")
    else:
        for job in archived_jobs:
            with st.container():
                st.markdown(f"""
                <div class="job-card" style="opacity: 0.85; background: #fafafa;">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div>
                            <h3 style="margin: 0 0 6px 0; color: #475569; font-size: 1.1rem;">
                                {job['title']}
                            </h3>
                            <p style="margin: 0 0 8px 0; color: #64748b; font-size: 0.9rem;">
                                🏢 <b>{job['company']}</b> &nbsp;•&nbsp; 📍 {job['location']} &nbsp;•&nbsp; 📅 {job['published_date']}
                            </p>
                        </div>
                        <div>
                            <span class="tag tag-status-archived">Archivée</span>
                        </div>
                    </div>
                    <p style="color: #64748b; font-size: 0.88rem; margin: 8px 0;">
                        {job['description'][:200]}...
                    </p>
                </div>
                """, unsafe_allow_html=True)

                c_rest1, c_rest2, c_rest3 = st.columns([1, 1, 2])
                with c_rest1:
                    if st.button("↩️ Restaurer dans Opportunités", key=f"rest_new_{job['id']}", use_container_width=True):
                        db.update_status(job["id"], "Nouvelle")
                        st.toast("Offre restaurée dans les Opportunités !")
                        st.rerun()
                with c_rest2:
                    if st.button("🎯 Déplacer vers À postuler", key=f"rest_apply_{job['id']}", use_container_width=True):
                        db.update_status(job["id"], "À postuler")
                        st.toast("Offre déplacée vers 'À postuler' !")
                        st.rerun()
                with c_rest3:
                    if job.get("url"):
                        st.link_button("🔗 Voir l'offre originale", job["url"], use_container_width=True)

                st.markdown("<hr style='margin: 8px 0 16px 0; border: none; border-top: 1px dashed #e2e8f0;'>", unsafe_allow_html=True)
