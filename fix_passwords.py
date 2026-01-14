#!/usr/bin/env python3
"""
Script pour générer les hashs bcrypt corrects pour config.yaml
"""
import sys
import os

# Ajouter le venv au path
venv_path = os.path.join(os.path.dirname(__file__), '..', '..', 'venv', 'lib', 'python3.9', 'site-packages')
sys.path.insert(0, venv_path)

try:
    import bcrypt
except ImportError:
    print("❌ Impossible d'importer bcrypt. Tentative avec streamlit-authenticator...")
    try:
        import streamlit_authenticator as stauth
        # Utiliser la méthode de hash de streamlit-authenticator
        passwords = ['admin123', 'florian123', 'manager123', 'viewer123']
        hashed_passwords = stauth.Hasher(passwords).generate()
        
        # Lire et mettre à jour config.yaml
        import yaml
        from pathlib import Path
        
        config_path = Path('config.yaml')
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        usernames = ['admin', 'florian', 'manager1', 'viewer']
        for username, hashed in zip(usernames, hashed_passwords):
            if username in config['credentials']['usernames']:
                config['credentials']['usernames'][username]['password'] = hashed
                print(f"✅ {username}: {hashed}")
        
        # Sauvegarder
        with open(config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
        
        print(f"\n✅ Fichier config.yaml mis à jour avec les hashs corrects !")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Erreur : {e}")
        sys.exit(1)

# Si bcrypt fonctionne directement
import yaml
from pathlib import Path

passwords = {
    'admin': 'admin123',
    'florian': 'florian123',
    'manager1': 'manager123',
    'viewer': 'viewer123'
}

print("🔐 Génération des hashs bcrypt pour les mots de passe\n")

config_path = Path('config.yaml')
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

for username, password in passwords.items():
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    hashed_str = hashed.decode('utf-8')
    
    if username in config['credentials']['usernames']:
        config['credentials']['usernames'][username]['password'] = hashed_str
        print(f"✅ {username}: {hashed_str}")

with open(config_path, 'w') as f:
    yaml.dump(config, f, default_flow_style=False, allow_unicode=True)

print(f"\n✅ Fichier config.yaml mis à jour avec les hashs corrects !")
