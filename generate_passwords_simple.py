#!/usr/bin/env python3
"""
Script simple pour générer les hashs avec streamlit-authenticator
"""
import streamlit_authenticator as stauth
import yaml

# Mots de passe à hasher
passwords = ['admin123', 'florian123', 'manager123', 'viewer123']
usernames = ['admin', 'florian', 'manager1', 'viewer']

print("🔐 Génération des hashs bcrypt pour les mots de passe\n")

# Générer les hashs avec streamlit-authenticator
hashed_passwords = stauth.Hasher(passwords).generate()

# Afficher les hashs
for username, pwd, hashed in zip(usernames, passwords, hashed_passwords):
    print(f"{username} ({pwd}): {hashed}")

print("\n✅ Copiez ces hashs dans config.yaml")
