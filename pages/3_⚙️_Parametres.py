# pages/3_⚙️_Parametres.py
"""
Page de paramètres et configuration utilisateur
"""
import streamlit as st
from utils.permissions import get_user_permissions, has_permission
from utils.audit import log_action, log_data_access

st.set_page_config(page_title="Paramètres", page_icon="⚙️", layout="wide")

# Vérification de base
if not st.session_state.get('authenticated', False):
    st.warning("⚠️ Veuillez vous connecter depuis la page d'accueil")
    st.stop()

# Log de l'accès à la page Paramètres
log_data_access("parametres", {"role": st.session_state.role, "user": st.session_state.get('username', 'unknown')})

# En-tête
st.title("⚙️ Paramètres")
st.caption(f"Connecté en tant que : **{st.session_state.name}** ({st.session_state.role})")

# Onglets
tab1, tab2, tab3 = st.tabs(["👤 Profil", "🔐 Sécurité", "📊 Permissions"])

with tab1:
    st.subheader("👤 Informations du profil")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_input("Nom d'utilisateur", value=st.session_state.username, disabled=True)
        st.text_input("Nom complet", value=st.session_state.name, disabled=True)
    
    with col2:
        st.text_input("Email", value=st.session_state.email, disabled=True)
        st.text_input("Rôle", value=st.session_state.role.upper(), disabled=True)
    
    st.divider()
    
    st.subheader("🎨 Préférences d'affichage")
    
    # Préférences (stockées dans session_state)
    theme = st.selectbox(
        "Thème",
        ["Clair", "Sombre", "Auto"],
        index=0
    )
    
    langue = st.selectbox(
        "Langue",
        ["Français", "English"],
        index=0
    )
    
    if st.button("💾 Enregistrer les préférences"):
        st.session_state.theme = theme
        st.session_state.langue = langue
        st.success("✅ Préférences enregistrées")

with tab2:
    st.subheader("🔐 Sécurité")
    
    st.info("ℹ️ Pour changer votre mot de passe, utilisez le menu dans la barre latérale")
    
    st.divider()
    
    st.subheader("📜 Historique des connexions")
    
    # Simulation d'historique
    import pandas as pd
    from datetime import datetime, timedelta
    
    historique = pd.DataFrame({
        'Date': [
            datetime.now() - timedelta(days=i) for i in range(5)
        ],
        'Adresse IP': ['192.168.1.100', '192.168.1.101', '192.168.1.100', '10.0.0.50', '192.168.1.100'],
        'Navigateur': ['Chrome', 'Firefox', 'Chrome', 'Safari', 'Chrome'],
        'Statut': ['✅ Succès', '✅ Succès', '✅ Succès', '❌ Échec', '✅ Succès']
    })
    
    st.dataframe(historique, use_container_width=True)
    
    if has_permission(st.session_state.role, "view_logs"):
        st.divider()
        st.subheader("📊 Logs système")
        st.info("🔑 Vous avez accès aux logs système (réservé aux administrateurs)")

with tab3:
    st.subheader("📊 Vos permissions")
    
    permissions = get_user_permissions(st.session_state.role)
    
    # Affichage des permissions
    st.markdown(f"**Vous disposez de {len(permissions)} permission(s) :**")
    
    # Mapping des permissions en français
    permission_labels = {
        "view_dashboard": "📊 Voir le dashboard",
        "view_sensitive_data": "💰 Voir les données sensibles",
        "edit_data": "✏️ Modifier les données",
        "delete_data": "🗑️ Supprimer des données",
        "export_all": "📥 Exporter toutes les données",
        "export_filtered": "📥 Exporter les données filtrées",
        "manage_users": "👥 Gérer les utilisateurs",
        "view_all_data": "👁️ Voir toutes les données",
        "view_logs": "📜 Voir les logs système",
        "view_department_data": "🏢 Voir les données du département",
        "view_team_data": "👥 Voir les données de l'équipe",
        "create_reports": "📄 Créer des rapports",
        "approve_requests": "✅ Approuver des demandes"
    }
    
    # Afficher les permissions sous forme de colonnes
    cols = st.columns(2)
    for idx, perm in enumerate(permissions):
        with cols[idx % 2]:
            label = permission_labels.get(perm, perm)
            st.success(f"✅ {label}")
    
    st.divider()
    
    # Comparaison des rôles
    st.subheader("🎭 Comparaison des rôles")
    
    roles_comparison = {
        "Admin": ["Accès complet", "Gestion utilisateurs", "Toutes les données", "Logs système"],
        "Analyst": ["Données département", "Données sensibles", "Export filtré", "Création rapports"],
        "Manager": ["Données équipe", "Modification données", "Export filtré", "Approbation demandes"],
        "Viewer": ["Lecture seule", "Dashboard", "Export agrégé"]
    }
    
    col1, col2, col3, col4 = st.columns(4)
    
    for col, (role, features) in zip([col1, col2, col3, col4], roles_comparison.items()):
        with col:
            if role.lower() == st.session_state.role:
                st.info(f"**{role}** 👈 Votre rôle")
            else:
                st.markdown(f"**{role}**")
            
            for feature in features:
                st.caption(f"• {feature}")
    
    st.divider()
    
    st.info("""
    💡 **Besoin de permissions supplémentaires ?**
    
    Contactez votre administrateur pour demander un changement de rôle.
    """)
