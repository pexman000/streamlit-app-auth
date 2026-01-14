# pages/2_📈_Analyses.py
"""
Page d'analyses avancées avec filtres et permissions
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.permissions import has_permission
from utils.data_access import filter_dataframe_for_display
from utils.audit import log_action, log_data_access, log_export

st.set_page_config(page_title="Analyses", page_icon="📈", layout="wide")

# Vérification de base
if not st.session_state.get('authenticated', False):
    st.warning("⚠️ Veuillez vous connecter depuis la page d'accueil")
    st.stop()

# Log de l'accès à la page Analyses
log_data_access("analyses", {"role": st.session_state.role, "user": st.session_state.get('username', 'unknown')})

# En-tête
st.title("📈 Analyses Avancées")
st.caption(f"Connecté en tant que : **{st.session_state.name}** ({st.session_state.role})")

# Charger les données
@st.cache_data
def load_data():
    return pd.read_csv("data/ventes.csv")

try:
    df_complet = load_data()
    
    # Filtrer les données selon le rôle
    df_utilisateur = filter_dataframe_for_display(
        df_complet,
        st.session_state.role,
        st.session_state.username
    )
    
    # Sidebar avec filtres
    with st.sidebar:
        st.header("🔍 Filtres")
        
        # Filtre par catégorie
        if 'categorie' in df_utilisateur.columns:
            categories = ['Toutes'] + list(df_utilisateur['categorie'].unique())
            categorie_selectionnee = st.selectbox("Catégorie", categories)
            
            if categorie_selectionnee != 'Toutes':
                df_utilisateur = df_utilisateur[df_utilisateur['categorie'] == categorie_selectionnee]
        
        # Filtre par date
        if 'date' in df_utilisateur.columns:
            df_utilisateur['date'] = pd.to_datetime(df_utilisateur['date'])
            date_min = df_utilisateur['date'].min()
            date_max = df_utilisateur['date'].max()
            
            date_range = st.date_input(
                "Période",
                value=(date_min, date_max),
                min_value=date_min,
                max_value=date_max
            )
            
            if len(date_range) == 2:
                df_utilisateur = df_utilisateur[
                    (df_utilisateur['date'] >= pd.to_datetime(date_range[0])) &
                    (df_utilisateur['date'] <= pd.to_datetime(date_range[1]))
                ]
        
        # Filtre par employé (si visible)
        if 'employe' in df_utilisateur.columns:
            employes = ['Tous'] + list(df_utilisateur['employe'].unique())
            employe_selectionne = st.selectbox("Employé", employes)
            
            if employe_selectionne != 'Tous':
                df_utilisateur = df_utilisateur[df_utilisateur['employe'] == employe_selectionne]
    
    # KPIs
    st.subheader("📊 Indicateurs clés")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📈 Nombre de ventes", len(df_utilisateur))
    
    with col2:
        if 'montant' in df_utilisateur.columns:
            st.metric("💰 Montant total", f"{df_utilisateur['montant'].sum():,.0f} €")
    
    with col3:
        if 'montant' in df_utilisateur.columns:
            st.metric("📊 Montant moyen", f"{df_utilisateur['montant'].mean():,.0f} €")
    
    with col4:
        if 'quantite' in df_utilisateur.columns:
            st.metric("📦 Quantité totale", f"{df_utilisateur['quantite'].sum():,.0f}")
    
    st.divider()
    
    # Analyses graphiques
    if has_permission(st.session_state.role, "view_sensitive_data"):
        st.subheader("📊 Analyse de la performance")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Top 5 des catégories
            if 'categorie' in df_utilisateur.columns and 'montant' in df_utilisateur.columns:
                top_categories = df_utilisateur.groupby('categorie')['montant'].sum().nlargest(5)
                fig = px.bar(
                    x=top_categories.values,
                    y=top_categories.index,
                    orientation='h',
                    title="Top 5 des catégories",
                    labels={'x': 'Montant (€)', 'y': 'Catégorie'}
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Répartition par département
            if 'departement' in df_utilisateur.columns and 'montant' in df_utilisateur.columns:
                fig = px.pie(
                    df_utilisateur.groupby('departement')['montant'].sum().reset_index(),
                    values='montant',
                    names='departement',
                    title="Répartition par département"
                )
                st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Analyse temporelle
    st.subheader("📅 Analyse temporelle")
    
    if 'date' in df_utilisateur.columns and 'montant' in df_utilisateur.columns:
        df_temp = df_utilisateur.copy()
        df_temp['date'] = pd.to_datetime(df_temp['date'])
        df_temp['mois'] = df_temp['date'].dt.to_period('M').astype(str)
        
        monthly_data = df_temp.groupby('mois')['montant'].sum().reset_index()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=monthly_data['mois'],
            y=monthly_data['montant'],
            mode='lines+markers',
            name='Montant mensuel',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title="Évolution mensuelle du chiffre d'affaires",
            xaxis_title="Mois",
            yaxis_title="Montant (€)",
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Tableau détaillé
    st.subheader("📋 Données détaillées")
    
    # Options d'affichage
    col1, col2 = st.columns([3, 1])
    with col1:
        search = st.text_input("🔍 Rechercher", placeholder="Rechercher dans les données...")
    with col2:
        nb_lignes = st.selectbox("Lignes par page", [10, 25, 50, 100], index=1)
    
    # Filtrer par recherche
    if search:
        mask = df_utilisateur.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)
        df_affiche = df_utilisateur[mask]
    else:
        df_affiche = df_utilisateur
    
    # Afficher le tableau
    st.dataframe(df_affiche.head(nb_lignes), use_container_width=True)
    st.caption(f"Affichage de {min(nb_lignes, len(df_affiche))} lignes sur {len(df_affiche)}")

except FileNotFoundError:
    st.error("❌ Fichier de données introuvable : `data/ventes.csv`")
except Exception as e:
    st.error(f"❌ Erreur : {e}")
