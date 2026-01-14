# generate_sample_data.py
"""
Script pour générer des données d'exemple pour l'application
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Configuration
np.random.seed(42)
n_rows = 200

# Générer les dates
start_date = datetime.now() - timedelta(days=180)
dates = [start_date + timedelta(days=i) for i in range(180)]
dates_sample = np.random.choice(dates, n_rows)

# Catégories
categories = ['Électronique', 'Vêtements', 'Alimentation', 'Maison', 'Sport', 'Livres']

# Départements
departements = ['Direction', 'Analyse', 'Ventes', 'Support']

# Employés par département
employes = {
    'Direction': ['Jean Directeur', 'Marie CEO'],
    'Analyse': ['David Chen', 'Emma Bernard', 'Frank Moreau'],
    'Ventes': ['Alice Martin', 'Bob Dupont', 'Claire Leroy'],
    'Support': ['Sophie Viewer', 'Thomas Support']
}

# Clients
clients = [
    'Client A', 'Client B', 'Client C', 'Client D', 'Client E',
    'Client F', 'Client G', 'Client H', 'Client I', 'Client J'
]

# Générer les données
data = []

for i in range(n_rows):
    # Sélectionner un département
    dept = np.random.choice(departements)
    
    # Sélectionner un employé du département
    employe = np.random.choice(employes[dept])
    
    # Générer les montants
    montant = np.random.randint(100, 5000)
    marge_pct = np.random.uniform(10, 40)
    cout = montant * (1 - marge_pct / 100)
    
    # Créer la ligne
    row = {
        'date': dates_sample[i].strftime('%Y-%m-%d'),
        'categorie': np.random.choice(categories),
        'montant': round(montant, 2),
        'quantite': np.random.randint(1, 20),
        'employe': employe,
        'departement': dept,
        'client': np.random.choice(clients),
        'marge': round(marge_pct, 1),
        'cout': round(cout, 2),
        'notes': f'Vente #{i+1:04d}'
    }
    
    data.append(row)

# Créer le DataFrame
df = pd.DataFrame(data)

# Trier par date
df = df.sort_values('date').reset_index(drop=True)

# Sauvegarder
df.to_csv('data/ventes.csv', index=False)

print(f"✅ Fichier créé : data/ventes.csv")
print(f"📊 Nombre de lignes : {len(df)}")
print(f"📋 Colonnes : {', '.join(df.columns)}")
print(f"\n📈 Aperçu des données :")
print(df.head(10))
print(f"\n💰 Statistiques :")
print(f"  - Montant total : {df['montant'].sum():,.2f} €")
print(f"  - Montant moyen : {df['montant'].mean():,.2f} €")
print(f"  - Marge moyenne : {df['marge'].mean():.1f}%")
print(f"\n🏢 Répartition par département :")
print(df.groupby('departement')['montant'].sum().sort_values(ascending=False))
