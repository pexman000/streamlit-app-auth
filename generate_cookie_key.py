#!/usr/bin/env python3
"""
Script pour générer une clé de cookie sécurisée
Utilisez cette clé pour remplacer cookie.key dans vos secrets Streamlit Cloud
"""

import secrets

# Générer une clé sécurisée de 32 bytes (256 bits)
cookie_key = secrets.token_urlsafe(32)

print("=" * 60)
print("🔐 Clé de cookie sécurisée générée")
print("=" * 60)
print()
print(f"Clé : {cookie_key}")
print()
print("📋 Copiez cette clé et utilisez-la dans vos secrets Streamlit Cloud :")
print()
print(f"[cookie]")
print(f"key = \"{cookie_key}\"")
print()
print("=" * 60)
print("⚠️  IMPORTANT : Gardez cette clé secrète et ne la commitez JAMAIS !")
print("=" * 60)
