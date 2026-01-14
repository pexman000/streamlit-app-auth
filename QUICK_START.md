# ⚡ Déploiement Rapide - Checklist

## 🎯 Étapes Rapides

### 1. Préparer Git (si pas déjà fait)

```bash
cd "/Users/teiva/streamlit-ambient/exos_j2 last/app_auth"
git init
git add .
git commit -m "Ready for Streamlit Cloud deployment"
```

### 2. Créer le Repository GitHub

1. Allez sur [github.com](https://github.com) → **New repository**
2. Nommez-le (ex: `streamlit-auth-app`)
3. **Ne cochez PAS** "Initialize with README"
4. Cliquez **Create repository**

### 3. Pousser le Code

```bash
# Remplacez par vos valeurs
git remote add origin https://github.com/VOTRE_USERNAME/VOTRE_REPO.git
git branch -M main
git push -u origin main
```

### 4. Déployer sur Streamlit Cloud

1. Allez sur [share.streamlit.io](https://share.streamlit.io)
2. **New app** → Sélectionnez votre repo
3. **Main file path** : `app.py`
4. **Advanced settings** → **Secrets** → Collez le contenu de `secrets.example.toml`
5. **IMPORTANT** : Changez `cookie.key` (utilisez `python generate_cookie_key.py`)
6. Cliquez **Deploy!**

### 5. Tester

Votre app sera à : `https://VOTRE_APP.streamlit.app`

Connectez-vous avec :
- **admin** / **admin123**
- **florian** / **florian123**

## 📝 Fichiers Créés

- ✅ `app.py` : Modifié pour utiliser `st.secrets` (compatible Streamlit Cloud)
- ✅ `.streamlit/config.toml` : Configuration Streamlit
- ✅ `secrets.example.toml` : Exemple de structure des secrets
- ✅ `DEPLOYMENT.md` : Guide complet de déploiement
- ✅ `generate_cookie_key.py` : Script pour générer une clé sécurisée

## ⚠️ Points Critiques

1. **Secrets** : Configurez-les dans Streamlit Cloud (Settings → Secrets)
2. **Cookie Key** : Changez-la par une valeur sécurisée
3. **Requirements.txt** : Déjà à jour ✅
4. **Gitignore** : `config.yaml` est déjà ignoré ✅

## 📚 Documentation Complète

Voir `DEPLOYMENT.md` pour le guide détaillé.

---

**Prêt à déployer ! 🚀**
