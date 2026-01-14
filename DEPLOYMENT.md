# 🚀 Guide de Déploiement sur Streamlit Cloud

Ce guide vous explique comment déployer l'application d'authentification sur Streamlit Cloud.

## 📋 Prérequis

1. **Compte GitHub** (gratuit)
2. **Compte Streamlit Cloud** (gratuit) : [share.streamlit.io](https://share.streamlit.io)
3. **Repository Git** avec votre code

## 🔧 Étapes de Déploiement

### 1. Préparer le Repository GitHub

#### 1.1 Initialiser Git (si pas déjà fait)

```bash
cd "/Users/teiva/streamlit-ambient/exos_j2 last/app_auth"
git init
git add .
git commit -m "Initial commit - App auth ready for deployment"
```

#### 1.2 Créer un Repository sur GitHub

1. Allez sur [github.com](https://github.com)
2. Cliquez sur **"New repository"**
3. Nommez-le (ex: `streamlit-auth-app`)
4. **Ne cochez PAS** "Initialize with README"
5. Cliquez sur **"Create repository"**

#### 1.3 Pousser le Code

```bash
# Remplacez VOTRE_USERNAME et VOTRE_REPO par vos valeurs
git remote add origin https://github.com/VOTRE_USERNAME/VOTRE_REPO.git
git branch -M main
git push -u origin main
```

### 2. Configurer les Secrets sur Streamlit Cloud

#### 2.1 Accéder à Streamlit Cloud

1. Allez sur [share.streamlit.io](https://share.streamlit.io)
2. Connectez-vous avec votre compte GitHub
3. Cliquez sur **"New app"**

#### 2.2 Configurer l'Application

- **Repository** : Sélectionnez votre repository
- **Branch** : `main` (ou la branche que vous utilisez)
- **Main file path** : `app.py`
- **App URL** : Choisissez un nom unique (ex: `mon-app-auth`)

#### 2.3 Configurer les Secrets

**IMPORTANT** : Les secrets sont nécessaires pour l'authentification !

1. Cliquez sur **"Advanced settings"**
2. Cliquez sur **"Secrets"**
3. Collez le contenu suivant (adaptez les valeurs) :

```toml
[credentials]
[credentials.usernames]
[credentials.usernames.admin]
email = "admin@company.com"
name = "Administrateur"
password = "$2b$12$hCI85O9QlkTTJZLy3F3fMOL98bv7RFsP4.N57bHbzM.ORrUxqoIAC"
role = "admin"

[credentials.usernames.florian]
email = "florian@company.com"
name = "Florian DUCHAT"
password = "$2b$12$M7wJRPwo/wske0.LbVo8vu4SwH/ruzrPvjFS5A7L89jM7sApRdw3u"
role = "analyst"

[credentials.usernames.manager1]
email = "manager@company.com"
name = "Marie Manager"
password = "$2b$12$09g9pnFTHCzP5i5w/E9GUe2T1i8YBaOECqPMeW4BO2.LgOJ5Lgz5m"
role = "manager"

[credentials.usernames.viewer]
email = "viewer@company.com"
name = "Utilisateur Lecture"
password = "$2b$12$h5TzAeOSuD1xHpx1N0Jf6.j1jQn.s.0Q3LUeFgvXL.I216as1.jRO"
role = "viewer"

[cookie]
expiry_days = 30
key = "CHANGEZ_CETTE_CLE_EN_PRODUCTION_avec_une_valeur_aleatoire_longue"
name = "streamlit_auth_cookie"

[preauthorized]
emails = ["nouveau@company.com"]
```

**⚠️ IMPORTANT** : 
- Changez la clé `cookie.key` par une valeur aléatoire longue et sécurisée
- Les mots de passe sont hashés avec bcrypt (ne les modifiez pas si vous voulez utiliser les comptes de démo)

#### 2.4 Générer une Nouvelle Clé de Cookie Sécurisée

Pour générer une clé sécurisée, utilisez Python :

```python
import secrets
print(secrets.token_urlsafe(32))
```

Copiez la valeur générée et remplacez `cookie.key` dans les secrets.

### 3. Déployer l'Application

1. Cliquez sur **"Deploy!"**
2. Attendez quelques secondes que l'application se déploie
3. Votre application sera accessible à : `https://VOTRE_APP.streamlit.app`

## 🔐 Comptes de Démonstration

Une fois déployé, vous pouvez vous connecter avec :

| Utilisateur | Mot de passe | Rôle |
|-------------|-------------|------|
| `admin` | `admin123` | Administrateur |
| `florian` | `florian123` | Analyste |
| `manager1` | `manager123` | Manager |
| `viewer` | `viewer123` | Lecteur |

## 📁 Structure des Fichiers Requis

Votre repository doit contenir :

```
app_auth/
├── app.py                    # ✅ Fichier principal
├── requirements.txt           # ✅ Dépendances Python
├── pages/                    # ✅ Pages de l'application
│   ├── 1_📊_Dashboard.py
│   ├── 2_📈_Analyses.py
│   └── 3_⚙️_Parametres.py
├── utils/                    # ✅ Modules utilitaires
│   ├── __init__.py
│   ├── audit.py
│   ├── data_access.py
│   └── permissions.py
├── data/                     # ✅ Données (optionnel)
│   └── ventes.csv
└── .streamlit/              # ✅ Configuration (optionnel)
    └── config.toml
```

## 🔄 Mises à Jour

Pour mettre à jour l'application :

1. Modifiez votre code localement
2. Committez et poussez vers GitHub :
   ```bash
   git add .
   git commit -m "Description des modifications"
   git push
   ```
3. Streamlit Cloud détecte automatiquement les changements et redéploie

## ⚠️ Points Importants

### Secrets vs Config.yaml

- **En local** : L'application utilise `config.yaml` si disponible
- **Sur Streamlit Cloud** : L'application utilise `st.secrets` (configuré via l'interface)
- **Les deux méthodes sont supportées** : Le code détecte automatiquement laquelle utiliser

### Limitations de Streamlit Cloud

1. **Modification de mot de passe** : Les modifications via l'interface ne sont pas persistées (les secrets sont en lecture seule)
2. **Création de comptes** : Les nouveaux comptes créés via l'interface ne sont pas persistés
3. **Solution** : Pour ajouter/modifier des utilisateurs, modifiez les secrets via l'interface Streamlit Cloud

### Sécurité

1. **Ne commitez JAMAIS** :
   - `config.yaml`
   - `.streamlit/secrets.toml`
   - Les mots de passe en clair

2. **Utilisez des clés sécurisées** :
   - Générez une clé de cookie unique et longue
   - Utilisez bcrypt pour hasher les mots de passe

3. **HTTPS** : Streamlit Cloud utilise automatiquement HTTPS

## 🐛 Dépannage

### L'application ne démarre pas

1. Vérifiez les logs dans Streamlit Cloud
2. Vérifiez que `requirements.txt` contient toutes les dépendances
3. Vérifiez que `app.py` est le bon fichier principal

### Erreur "Configuration non trouvée"

1. Vérifiez que les secrets sont bien configurés dans Streamlit Cloud
2. Vérifiez la structure des secrets (doit correspondre à `secrets.example.toml`)

### Erreur d'authentification

1. Vérifiez que les mots de passe hashés dans les secrets sont corrects
2. Vérifiez que la structure `credentials.usernames` est correcte

### Les données ne s'affichent pas

1. Vérifiez que `data/ventes.csv` existe dans le repository
2. Ou générez les données avec `generate_sample_data.py` avant de déployer

## 📚 Ressources

- [Documentation Streamlit Cloud](https://docs.streamlit.io/streamlit-community-cloud)
- [Gestion des Secrets](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management)
- [streamlit-authenticator](https://github.com/mkhorasani/Streamlit-Authenticator)

## ✅ Checklist de Déploiement

- [ ] Code poussé sur GitHub
- [ ] Repository créé sur Streamlit Cloud
- [ ] Secrets configurés (credentials, cookie, preauthorized)
- [ ] Clé de cookie changée (valeur sécurisée)
- [ ] `requirements.txt` à jour
- [ ] `app.py` est le fichier principal
- [ ] Données présentes (ou générées)
- [ ] Application déployée et accessible
- [ ] Test de connexion avec un compte de démo

---

**Bon déploiement ! 🚀**

*Dernière mise à jour : Janvier 2026*
