# app.py
"""
Application Streamlit avec authentification et gestion des permissions
"""
import streamlit as st
import streamlit_authenticator as stauth
import yaml
import copy
from yaml.loader import SafeLoader
from utils.audit import log_action

# Configuration de la page
st.set_page_config(
    page_title="Application Sécurisée",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Fonction helper pour convertir st.secrets en dictionnaire Python
def secrets_to_dict(secrets_obj):
    """Convertit un objet st.secrets en dictionnaire Python modifiable"""
    if hasattr(secrets_obj, 'to_dict'):
        # Si l'objet a une méthode to_dict, l'utiliser
        return secrets_obj.to_dict()
    elif isinstance(secrets_obj, dict):
        # Si c'est déjà un dict, créer une copie profonde
        return {k: secrets_to_dict(v) for k, v in secrets_obj.items()}
    elif hasattr(secrets_obj, 'keys'):
        # Si c'est un objet dict-like (comme st.secrets), convertir récursivement
        return {k: secrets_to_dict(secrets_obj[k]) for k in secrets_obj.keys()}
    else:
        # Valeur primitive, retourner telle quelle
        return secrets_obj

# Charger la configuration
# Sur Streamlit Cloud, utiliser st.secrets
# En local, utiliser config.yaml
config = None

# Essayer d'abord avec st.secrets (Streamlit Cloud)
try:
    _ = st.secrets['credentials']  # Vérifier si credentials existe
    # Convertir st.secrets en dictionnaires Python (st.secrets est en lecture seule)
    credentials_dict = secrets_to_dict(st.secrets['credentials'])
    cookie_dict = secrets_to_dict(st.secrets['cookie'])
    # Récupérer preauthorized avec fallback
    try:
        preauthorized_dict = secrets_to_dict(st.secrets['preauthorized'])
    except (KeyError, AttributeError):
        preauthorized_dict = {'emails': []}
    config = {
        'credentials': credentials_dict,
        'cookie': cookie_dict,
        'preauthorized': preauthorized_dict
    }
except (KeyError, AttributeError, TypeError):
    # Secrets non configurés, essayer config.yaml (local)
    try:
        with open('config.yaml') as file:
            config = yaml.load(file, Loader=SafeLoader)
    except FileNotFoundError:
        config = None

# Si la configuration n'est toujours pas chargée
if config is None:
    st.error("""
    ❌ **Configuration non trouvée**
    
    **Pour Streamlit Cloud :** Veuillez configurer les secrets :
    
    1. Allez sur [share.streamlit.io](https://share.streamlit.io)
    2. Sélectionnez votre application
    3. Cliquez sur **"⋮"** (menu) → **"Settings"** → **"Secrets"**
    4. Collez la configuration au format TOML (voir `secrets.example.toml`)
    
    **Exemple de configuration minimale :**
    ```toml
    [credentials]
    [credentials.usernames]
    [credentials.usernames.admin]
    email = "admin@example.com"
    name = "Admin"
    password = "$2b$12$..."
    role = "admin"
    
    [cookie]
    expiry_days = 30
    key = "votre_cle_secrete_aleatoire_longue"
    name = "streamlit_auth_cookie"
    
    [preauthorized]
    emails = []
    ```
    
    Pour plus de détails, consultez `DEPLOYMENT.md` ou `secrets.example.toml`.
    """)
    st.stop()

# Créer l'objet authenticator
# Note : preauthorized n'est plus un paramètre de Authenticate dans les versions récentes
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# Afficher le formulaire de connexion
# Essayer uniquement le format location='main'
name = None
authentication_status = None
username = None

# Appeler login() avec location='main' (format correct)
authenticator.login(location='main')

# Récupérer les informations depuis st.session_state
name = st.session_state.get('name')
authentication_status = st.session_state.get('authentication_status')
username = st.session_state.get('username')
# Gérer les différents états d'authentification
if authentication_status == False:
    st.error('❌ Nom d\'utilisateur ou mot de passe incorrect')
    # Log de tentative de connexion échouée
    log_action("LOGIN_FAILED", f"username_attempt={username if username else 'unknown'}")
    
elif authentication_status == None:
    st.warning('👆 Veuillez entrer vos identifiants')
    st.info("""
    ### 🔑 Comptes de démonstration
    
    | Utilisateur | Mot de passe | Rôle |
    |-------------|--------------|------|
    | admin | admin123 | Administrateur |
    | florian | florian123 | Analyste |
    | manager1 | manager123 | Manager |
    | viewer | viewer123 | Lecteur |
    """)
    
elif authentication_status:
    # ✅ UTILISATEUR CONNECTÉ
    
    # Récupérer le rôle de l'utilisateur
    user_role = config['credentials']['usernames'][username]['role']
    user_email = config['credentials']['usernames'][username]['email']
    
    # Stocker les infos dans session_state pour les autres pages
    st.session_state['authenticated'] = True
    st.session_state['username'] = username
    st.session_state['name'] = name
    st.session_state['role'] = user_role
    st.session_state['email'] = user_email
    
    # Log de connexion réussie
    log_action("LOGIN_SUCCESS", f"role={user_role}")
    
    # Sidebar avec infos utilisateur
    with st.sidebar:
        st.success(f"👤 Connecté : **{name}**")
        st.caption(f"📧 {user_email}")
        st.caption(f"🎭 Rôle : **{user_role.upper()}**")
        
        st.divider()
        
        # Bouton de déconnexion
        logout_button = authenticator.logout('🚪 Déconnexion', 'sidebar')
        if logout_button:
            # Log de déconnexion
            log_action("LOGOUT", f"user={username} role={user_role}")
        
        st.divider()
        
        # Réinitialisation de mot de passe
        with st.expander("🔄 Changer le mot de passe"):
            try:
                if authenticator.reset_password(username, 'Réinitialiser'):
                    st.success('✅ Mot de passe modifié avec succès')
                    # Log du changement de mot de passe
                    log_action("PASSWORD_RESET", f"user={username}")
                    # Sauvegarder la nouvelle config (uniquement en local)
                    # Sur Streamlit Cloud, les secrets sont gérés via l'interface
                    try:
                        with open('config.yaml', 'w') as file:
                            yaml.dump(config, file, default_flow_style=False)
                    except Exception:
                        st.warning("⚠️ Les modifications de mot de passe ne sont pas persistées sur Streamlit Cloud. Utilisez l'interface de gestion des secrets.")
            except Exception as e:
                st.error(f"❌ Erreur : {e}")
                log_action("PASSWORD_RESET_FAILED", f"user={username} error={str(e)}")
    
    # Contenu principal de l'application
    st.title(f"🏠 Bienvenue, {name} !")
    
    st.markdown(f"""
    ### 📋 Informations de votre compte
    
    | Information | Valeur |
    |-------------|--------|
    | **Utilisateur** | {username} |
    | **Nom complet** | {name} |
    | **Email** | {user_email} |
    | **Rôle** | {user_role.upper()} |
    """)
    
    # Affichage conditionnel selon le rôle
    st.divider()
    
    if user_role == 'admin':
        st.info("🔑 **Administrateur** : Vous avez accès à toutes les fonctionnalités")
        st.markdown("""
        **Vos permissions :**
        - ✅ Voir toutes les données
        - ✅ Modifier et supprimer des données
        - ✅ Exporter toutes les données
        - ✅ Gérer les utilisateurs
        - ✅ Voir les logs système
        """)
        
    elif user_role == 'analyst':
        st.info("📊 **Analyste** : Vous avez accès aux analyses et rapports de votre département")
        st.markdown("""
        **Vos permissions :**
        - ✅ Voir les données de votre département
        - ✅ Voir les données sensibles
        - ✅ Exporter les données filtrées
        - ✅ Créer des rapports
        """)
        
    elif user_role == 'manager':
        st.info("👥 **Manager** : Vous avez accès aux données de votre équipe")
        st.markdown("""
        **Vos permissions :**
        - ✅ Voir les données de votre équipe
        - ✅ Modifier les données
        - ✅ Exporter les données filtrées
        - ✅ Approuver les demandes
        """)
        
    else:  # viewer
        st.info("👁️ **Lecteur** : Vous avez un accès en lecture seule")
        st.markdown("""
        **Vos permissions :**
        - ✅ Voir le dashboard
        - ✅ Exporter les données filtrées (agrégées)
        """)
    
    st.divider()
    
    # Navigation vers les pages
    st.subheader("📱 Navigation")
    st.markdown("""
    Utilisez le menu latéral pour accéder aux différentes pages :
    - **📊 Dashboard** : Visualisations et données selon vos permissions
    - **📈 Analyses** : Analyses détaillées de vos données
    - **⚙️ Paramètres** : Configuration de votre compte
    """)

# Formulaire d'inscription (si non connecté)
if not authentication_status:
    st.divider()
    with st.expander("📝 Créer un nouveau compte"):
        try:
            # Dans les nouvelles versions, preauthorization est un paramètre de register_user
            # Le premier argument positionnel (nom du formulaire) a été retiré
            # Vérifier si l'email est pré-autorisé depuis config.yaml
            preauthorized_emails = config.get('preauthorized', {}).get('emails', [])
            # preauthorization=True si l'email est dans la liste, False sinon
            if authenticator.register_user(preauthorization=len(preauthorized_emails) > 0):
                st.success('✅ Compte créé avec succès ! Vous pouvez maintenant vous connecter.')
                # Log de l'inscription
                log_action("USER_REGISTER", "new_user_registered")
                # Sauvegarder la nouvelle config (uniquement en local)
                try:
                    with open('config.yaml', 'w') as file:
                        yaml.dump(config, file, default_flow_style=False)
                except Exception:
                    st.warning("⚠️ Les nouveaux utilisateurs ne sont pas persistés sur Streamlit Cloud. Utilisez l'interface de gestion des secrets.")
        except Exception as e:
            st.error(f"❌ Erreur lors de la création du compte : {e}")
            log_action("USER_REGISTER_FAILED", f"error={str(e)}")

# Mot de passe oublié (si non connecté)
if not authentication_status:
    with st.expander("❓ Mot de passe ou nom d'utilisateur oublié"):
        try:
            username_forgot, email_forgot, new_password = authenticator.forgot_password('Récupération')
            if username_forgot:
                st.success(f'✅ Nouveau mot de passe généré')
                st.info(f"📧 Un email a été envoyé à {email_forgot} avec votre nouveau mot de passe : `{new_password}`")
                st.warning("⚠️ En production, envoyez ce mot de passe par email et ne l'affichez pas !")
                # Log de la récupération de mot de passe
                log_action("PASSWORD_RECOVERY", f"username={username_forgot} email={email_forgot}")
                # Sauvegarder la config (uniquement en local)
                try:
                    with open('config.yaml', 'w') as file:
                        yaml.dump(config, file, default_flow_style=False)
                except Exception:
                    st.warning("⚠️ Les modifications ne sont pas persistées sur Streamlit Cloud. Utilisez l'interface de gestion des secrets.")
        except Exception as e:
            st.error(f"❌ Erreur : {e}")
            log_action("PASSWORD_RECOVERY_FAILED", f"error={str(e)}")
        
        try:
            username_forgot, email_forgot = authenticator.forgot_username('Récupération nom d\'utilisateur')
            if username_forgot:
                st.success(f'✅ Votre nom d\'utilisateur est : `{username_forgot}`')
                st.info(f"📧 Un email a été envoyé à {email_forgot}")
                # Log de la récupération de nom d'utilisateur
                log_action("USERNAME_RECOVERY", f"email={email_forgot}")
        except Exception as e:
            st.error(f"❌ Erreur : {e}")
            log_action("USERNAME_RECOVERY_FAILED", f"error={str(e)}")