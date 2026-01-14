# 🔐 Application Streamlit avec Authentification et Permissions

Application complète démontrant l'authentification utilisateur, la gestion des permissions basée sur les rôles, et l'accès personnalisé aux données dans Streamlit.

## 📋 Table des matières

- [Fonctionnalités](#fonctionnalités)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
- [Rôles et Permissions](#rôles-et-permissions)
- [Structure du projet](#structure-du-projet)
- [Sécurité](#sécurité)

## ✨ Fonctionnalités

### 🔐 Authentification
- ✅ Connexion/Déconnexion sécurisée
- ✅ Gestion des sessions avec cookies
- ✅ Réinitialisation de mot de passe
- ✅ Création de nouveaux comptes
- ✅ Récupération de mot de passe/nom d'utilisateur oublié

### 🎭 Gestion des rôles et permissions
- ✅ 4 rôles prédéfinis : Admin, Analyst, Manager, Viewer
- ✅ Permissions granulaires par rôle
- ✅ Contrôle d'accès aux pages et fonctionnalités
- ✅ Vérification des permissions en temps réel

### 📊 Accès personnalisé aux données
- ✅ Filtrage automatique des données selon le rôle
- ✅ Colonnes visibles adaptées aux permissions
- ✅ Données départementales pour les analystes
- ✅ Données d'équipe pour les managers
- ✅ Données agrégées pour les lecteurs

### 📈 Visualisations et analyses
- ✅ Dashboard interactif avec KPIs
- ✅ Graphiques Plotly dynamiques
- ✅ Filtres avancés (catégorie, date, employé)
- ✅ Export de données selon les permissions

## 🏗️ Architecture

```
app_auth/
├── app.py                      # Page principale avec authentification
├── config.yaml                 # Configuration des utilisateurs (NE PAS COMMITER)
├── generate_sample_data.py     # Script de génération de données
├── .gitignore                  # Fichiers à ignorer
├── README.md                   # Ce fichier
│
├── utils/                      # Modules utilitaires
│   ├── __init__.py
│   ├── permissions.py          # Gestion des permissions
│   └── data_access.py          # Filtrage des données par rôle
│
├── pages/                      # Pages de l'application
│   ├── 1_📊_Dashboard.py       # Dashboard avec données filtrées
│   ├── 2_📈_Analyses.py        # Analyses avancées
│   └── 3_⚙️_Parametres.py      # Paramètres utilisateur
│
├── data/                       # Données de l'application
│   ├── .gitkeep
│   └── ventes.csv              # Données d'exemple
│
└── .streamlit/                 # Configuration Streamlit (optionnel)
    └── config.toml
```

## 🚀 Installation

### Prérequis
- Python 3.8+
- pip

### Étapes

1. **Cloner ou naviguer vers le dossier**
```bash
cd /Users/teiva/streamlit-ambient/app_auth
```

2. **Créer et activer l'environnement virtuel**

**macOS/Linux :**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows :**
```cmd
python -m venv venv
venv\Scripts\activate
```

3. **Installer les dépendances**
```bash
pip install streamlit streamlit-authenticator pandas numpy plotly pyyaml
```

4. **Générer les données d'exemple**
```bash
python generate_sample_data.py
```

## ⚙️ Configuration

### 1. Configuration des utilisateurs (`config.yaml`)

Le fichier `config.yaml` contient les informations d'authentification. **⚠️ Ne jamais commiter ce fichier !**

```yaml
credentials:
  usernames:
    admin:
      email: admin@company.com
      name: Administrateur
      password: $2b$12$...  # Hash bcrypt
      role: admin
```

### 2. Générer des mots de passe hashés

Pour créer un nouveau mot de passe hashé :

```python
import bcrypt

password = "mon_mot_de_passe"
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
print(hashed.decode('utf-8'))
```

### 3. Ajouter un nouvel utilisateur

Éditez `config.yaml` et ajoutez :

```yaml
nouveau_user:
  email: user@company.com
  name: Nom Complet
  password: $2b$12$...  # Hash du mot de passe
  role: analyst  # admin, analyst, manager, ou viewer
```

## 🎮 Utilisation

### Lancer l'application

```bash
streamlit run app.py
```

L'application sera accessible à : `http://localhost:8501`

### Comptes de démonstration

| Utilisateur | Mot de passe | Rôle | Accès |
|-------------|--------------|------|-------|
| `admin` | `admin123` | Administrateur | Toutes les données |
| `florian` | `florian123` | Analyste | Données du département Analyse |
| `manager1` | `manager123` | Manager | Données de son équipe |
| `viewer` | `viewer123` | Lecteur | Données agrégées uniquement |

### Navigation

1. **Page d'accueil** : Connexion et informations du compte
2. **📊 Dashboard** : Visualisations et KPIs selon vos permissions
3. **📈 Analyses** : Analyses avancées avec filtres
4. **⚙️ Paramètres** : Gestion du profil et des préférences

## 🎭 Rôles et Permissions

### 👑 Admin (Administrateur)
**Permissions :**
- ✅ Voir toutes les données
- ✅ Modifier et supprimer des données
- ✅ Exporter toutes les données
- ✅ Gérer les utilisateurs
- ✅ Voir les logs système

**Accès aux données :** Toutes les données sans restriction

### 📊 Analyst (Analyste)
**Permissions :**
- ✅ Voir les données de son département
- ✅ Voir les données sensibles (marges, coûts)
- ✅ Exporter les données filtrées
- ✅ Créer des rapports

**Accès aux données :** Données de son département uniquement

### 👥 Manager
**Permissions :**
- ✅ Voir les données de son équipe
- ✅ Modifier les données
- ✅ Exporter les données filtrées
- ✅ Approuver des demandes

**Accès aux données :** Données des membres de son équipe

### 👁️ Viewer (Lecteur)
**Permissions :**
- ✅ Voir le dashboard
- ✅ Exporter les données agrégées

**Accès aux données :** Données agrégées uniquement (pas de détails individuels)

## 📊 Gestion des données

### Filtrage automatique

Le module `utils/data_access.py` filtre automatiquement les données selon le rôle :

```python
from utils.data_access import filter_dataframe_for_display

# Filtre les lignes ET les colonnes selon le rôle
df_utilisateur = filter_dataframe_for_display(
    df_complet,
    st.session_state.role,
    st.session_state.username
)
```

### Colonnes visibles par rôle

| Colonne | Admin | Analyst | Manager | Viewer |
|---------|-------|---------|---------|--------|
| date | ✅ | ✅ | ✅ | ❌ |
| categorie | ✅ | ✅ | ✅ | ✅ |
| montant | ✅ | ✅ | ✅ | ✅ |
| quantite | ✅ | ✅ | ✅ | ✅ |
| employe | ✅ | ✅ | ✅ | ❌ |
| client | ✅ | ✅ | ✅ | ❌ |
| marge | ✅ | ✅ | ✅ | ❌ |
| cout | ✅ | ❌ | ❌ | ❌ |
| notes | ✅ | ❌ | ❌ | ❌ |
| departement | ✅ | ✅ | ✅ | ❌ |

## 🔒 Sécurité

### ✅ Bonnes pratiques implémentées

1. **Mots de passe hashés** : Utilisation de bcrypt pour le hashing
2. **Gestion des sessions** : Cookies sécurisés avec expiration
3. **Contrôle d'accès** : Vérification des permissions à chaque page
4. **Filtrage des données** : Accès limité selon le rôle
5. **Configuration externe** : Secrets dans `config.yaml` (non versionné)

### ⚠️ Recommandations pour la production

1. **Variables d'environnement** : Utiliser `.streamlit/secrets.toml` ou des variables d'environnement
2. **HTTPS** : Toujours utiliser HTTPS en production
3. **Clé de cookie unique** : Changer la clé dans `config.yaml`
4. **Logs** : Implémenter un système de logs pour l'audit
5. **Rate limiting** : Limiter les tentatives de connexion
6. **2FA** : Ajouter l'authentification à deux facteurs
7. **Base de données** : Stocker les utilisateurs dans une BDD sécurisée

### 🚫 Fichiers à ne jamais commiter

```gitignore
config.yaml
.streamlit/secrets.toml
.env
```

## 🛠️ Personnalisation

### Ajouter une nouvelle permission

1. **Éditer `utils/permissions.py`** :
```python
ROLE_PERMISSIONS = {
    "admin": [
        # ... permissions existantes
        "ma_nouvelle_permission"
    ]
}
```

2. **Utiliser la permission** :
```python
from utils.permissions import has_permission

if has_permission(st.session_state.role, "ma_nouvelle_permission"):
    # Code protégé
    st.button("Action réservée")
```

### Ajouter un nouveau rôle

1. **Éditer `utils/permissions.py`** :
```python
class Role(Enum):
    # ... rôles existants
    NOUVEAU_ROLE = "nouveau_role"

ROLE_PERMISSIONS = {
    # ... permissions existantes
    "nouveau_role": ["permission1", "permission2"]
}
```

2. **Ajouter l'utilisateur dans `config.yaml`** avec le nouveau rôle

## 📚 Ressources

- [Documentation Streamlit](https://docs.streamlit.io)
- [streamlit-authenticator](https://github.com/mkhorasani/Streamlit-Authenticator)
- [Plotly](https://plotly.com/python/)
- [Pandas](https://pandas.pydata.org/)

## 🤝 Support

Pour toute question ou problème :
1. Vérifier que toutes les dépendances sont installées
2. Vérifier que `config.yaml` est correctement configuré
3. Vérifier que les données d'exemple ont été générées
4. Consulter les logs dans le terminal

## 📝 Licence

Ce projet est un exemple pédagogique pour la formation Streamlit.

---

**Développé pour la formation Streamlit - Ambient IT**

*Dernière mise à jour : Janvier 2026*
