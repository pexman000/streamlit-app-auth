# pages/1_📊_Dashboard.py
"""
Page Dashboard avec permissions et accès aux données personnalisées
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.permissions import has_permission
from utils.data_access import filter_dataframe_for_display, can_export_data
from utils.audit import log_action, log_data_access, log_export

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

# Vérification de base
if not st.session_state.get('authenticated', False):
    st.warning("⚠️ Veuillez vous connecter depuis la page d'accueil")
    st.stop()

# Vérification de permission
if not has_permission(st.session_state.role, "view_dashboard"):
    st.error("🚫 Vous n'avez pas accès à cette page")
    log_action("ACCESS_DENIED", f"page=dashboard user={st.session_state.get('username', 'unknown')} role={st.session_state.get('role', 'unknown')}")
    st.stop()

# Log de l'accès au dashboard
log_data_access("dashboard", {"role": st.session_state.role})

# En-tête
st.title("📊 Dashboard")
st.caption(f"Connecté en tant que : **{st.session_state.name}** ({st.session_state.role})")

# Charger les données
@st.cache_data
def load_data():
    """Charge les données depuis le fichier CSV"""
    return pd.read_csv("data/ventes.csv")

try:
    df_complet = load_data()
    
    # Filtrer les données selon le rôle et l'utilisateur
    df_utilisateur = filter_dataframe_for_display(
        df_complet,
        st.session_state.role,
        st.session_state.username
    )
    
    # Afficher les informations sur les données
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 Lignes visibles", len(df_utilisateur))
    with col2:
        st.metric("📋 Colonnes visibles", len(df_utilisateur.columns))
    with col3:
        if 'montant' in df_utilisateur.columns:
            total = df_utilisateur['montant'].sum()
            st.metric("💰 Total", f"{total:,.0f} €")
    
    st.divider()
    
    # Sections conditionnelles selon les permissions
    if has_permission(st.session_state.role, "view_sensitive_data"):
        # Log de l'accès aux données sensibles
        log_action("VIEW_SENSITIVE_DATA", f"table=ventes role={st.session_state.role}")
        st.subheader("💰 Données financières détaillées")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if 'montant' in df_utilisateur.columns:
                st.metric("Chiffre d'affaires", f"{df_utilisateur['montant'].sum():,.0f} €")
        with col2:
            if 'marge' in df_utilisateur.columns:
                marge_moyenne = df_utilisateur['marge'].mean()
                st.metric("Marge moyenne", f"{marge_moyenne:.1f}%")
        with col3:
            if 'cout' in df_utilisateur.columns:
                cout_total = df_utilisateur['cout'].sum()
                st.metric("Coûts totaux", f"{cout_total:,.0f} €")
        with col4:
            if 'marge' in df_utilisateur.columns and 'montant' in df_utilisateur.columns:
                benefice = df_utilisateur['montant'].sum() - df_utilisateur.get('cout', pd.Series([0])).sum()
                st.metric("Bénéfice", f"{benefice:,.0f} €")
    else:
        st.info("📊 Données financières détaillées non disponibles pour votre rôle")
    
    st.divider()
    
    # Graphiques
    st.subheader("📈 Visualisations")
    
    tab1, tab2, tab3 = st.tabs(["📊 Par catégorie", "📅 Évolution", "👥 Par employé"])
    
    with tab1:
        if 'categorie' in df_utilisateur.columns and 'montant' in df_utilisateur.columns:
            fig = px.bar(
                df_utilisateur.groupby('categorie')['montant'].sum().reset_index(),
                x='categorie',
                y='montant',
                title="Montant par catégorie",
                labels={'montant': 'Montant (€)', 'categorie': 'Catégorie'}
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Données insuffisantes pour ce graphique")
    
    with tab2:
        if 'date' in df_utilisateur.columns and 'montant' in df_utilisateur.columns:
            df_temp = df_utilisateur.copy()
            df_temp['date'] = pd.to_datetime(df_temp['date'])
            fig = px.line(
                df_temp.groupby('date')['montant'].sum().reset_index(),
                x='date',
                y='montant',
                title="Évolution du montant",
                labels={'montant': 'Montant (€)', 'date': 'Date'}
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Données insuffisantes pour ce graphique")
    
    with tab3:
        if 'employe' in df_utilisateur.columns and 'montant' in df_utilisateur.columns:
            fig = px.pie(
                df_utilisateur.groupby('employe')['montant'].sum().reset_index(),
                values='montant',
                names='employe',
                title="Répartition par employé"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Données non disponibles pour votre rôle")
    
    st.divider()
    
    # Tableau de données
    st.subheader("📋 Données détaillées")
    st.dataframe(df_utilisateur, use_container_width=True)
    
    st.divider()
    
    # Boutons d'action conditionnels
    st.subheader("⚡ Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if has_permission(st.session_state.role, "export_all"):
            if st.button("📥 Exporter toutes les données", type="primary"):
                csv = df_complet.to_csv(index=False)
                st.download_button(
                    label="💾 Télécharger CSV complet",
                    data=csv,
                    file_name="export_complet.csv",
                    mime="text/csv"
                )
                st.success("✅ Export complet disponible")
                # Log de l'export
                log_export("csv", len(df_complet))
        elif can_export_data(st.session_state.role, "filtered"):
            if st.button("📥 Exporter mes données", type="primary"):
                csv = df_utilisateur.to_csv(index=False)
                st.download_button(
                    label="💾 Télécharger CSV filtré",
                    data=csv,
                    file_name="export_filtre.csv",
                    mime="text/csv"
                )
                st.success("✅ Export filtré disponible")
                # Log de l'export filtré
                log_export("csv_filtered", len(df_utilisateur))
    
    with col2:
        if has_permission(st.session_state.role, "edit_data"):
            if st.button("✏️ Modifier les données"):
                st.session_state.edit_mode = True
                st.info("Mode édition activé (fonctionnalité à implémenter)")
    
    with col3:
        if has_permission(st.session_state.role, "delete_data"):
            if st.button("🗑️ Supprimer", type="secondary"):
                st.warning("⚠️ Fonctionnalité de suppression (à implémenter)")

except FileNotFoundError:
    st.error("❌ Fichier de données introuvable : `data/ventes.csv`")
    st.info("Veuillez créer le fichier de données d'exemple")
except Exception as e:
    st.error(f"❌ Erreur lors du chargement des données : {e}")
