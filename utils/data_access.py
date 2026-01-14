# utils/data_access.py
"""
Module de gestion de l'accès aux données selon les rôles
"""
import pandas as pd
import streamlit as st
from typing import List


def get_user_department(username: str) -> str:
    """
    Retourne le département d'un utilisateur
    
    Args:
        username: Nom d'utilisateur
        
    Returns:
        Nom du département
    """
    # Mapping utilisateur -> département
    user_departments = {
        "admin": "Direction",
        "florian": "Analyse",
        "manager1": "Ventes",
        "viewer": "Support"
    }
    return user_departments.get(username, "Inconnu")


def get_team_members(username: str) -> List[str]:
    """
    Retourne les membres de l'équipe d'un manager
    
    Args:
        username: Nom d'utilisateur du manager
        
    Returns:
        Liste des noms des membres de l'équipe
    """
    # Mapping manager -> membres d'équipe
    team_structure = {
        "manager1": ["Alice Martin", "Bob Dupont", "Claire Leroy"],
        "florian": ["David Chen", "Emma Bernard", "Frank Moreau"]
    }
    return team_structure.get(username, [])


def get_filtered_data(df: pd.DataFrame, user_role: str, username: str) -> pd.DataFrame:
    """
    Filtre les données selon le rôle et l'utilisateur
    
    - ADMIN : Toutes les données
    - ANALYST : Données de son département
    - MANAGER : Données de son équipe
    - VIEWER : Données agrégées uniquement
    
    Args:
        df: DataFrame complet
        user_role: Rôle de l'utilisateur
        username: Nom d'utilisateur
        
    Returns:
        DataFrame filtré selon les permissions
    """
    if user_role == "admin":
        # Admin voit tout
        return df
    
    elif user_role == "analyst":
        # Analyst voit son département
        user_dept = get_user_department(username)
        if 'departement' in df.columns:
            return df[df['departement'] == user_dept]
        return df
    
    elif user_role == "manager":
        # Manager voit son équipe
        team_members = get_team_members(username)
        if 'employe' in df.columns:
            return df[df['employe'].isin(team_members)]
        return df
    
    else:  # viewer
        # Viewer voit uniquement des agrégats (pas de détails)
        if 'categorie' in df.columns and 'montant' in df.columns:
            return df.groupby('categorie').agg({
                'montant': 'sum',
                'quantite': 'sum' if 'quantite' in df.columns else 'count'
            }).reset_index()
        return df


def get_visible_columns(user_role: str) -> List[str]:
    """
    Retourne les colonnes visibles selon le rôle
    
    Args:
        user_role: Rôle de l'utilisateur
        
    Returns:
        Liste des noms de colonnes visibles
    """
    base_columns = ['date', 'categorie', 'montant']
    
    if user_role == "admin":
        return base_columns + ['employe', 'client', 'marge', 'cout', 'notes', 'departement']
    
    elif user_role in ["analyst", "manager"]:
        return base_columns + ['employe', 'client', 'marge', 'departement']
    
    else:  # viewer
        return ['categorie', 'montant', 'quantite']


def filter_dataframe_for_display(df: pd.DataFrame, user_role: str, username: str) -> pd.DataFrame:
    """
    Filtre et prépare un DataFrame pour l'affichage selon les permissions
    
    Args:
        df: DataFrame complet
        user_role: Rôle de l'utilisateur
        username: Nom d'utilisateur
        
    Returns:
        DataFrame prêt pour l'affichage
    """
    # Filtrer les lignes selon le rôle
    df_filtered = get_filtered_data(df, user_role, username)
    
    # Filtrer les colonnes selon le rôle
    visible_columns = get_visible_columns(user_role)
    
    # Garder seulement les colonnes qui existent dans le DataFrame
    available_columns = [col for col in visible_columns if col in df_filtered.columns]
    
    return df_filtered[available_columns]


def can_export_data(user_role: str, export_type: str = "filtered") -> bool:
    """
    Vérifie si un utilisateur peut exporter des données
    
    Args:
        user_role: Rôle de l'utilisateur
        export_type: Type d'export ("all" ou "filtered")
        
    Returns:
        True si l'export est autorisé, False sinon
    """
    if export_type == "all":
        return user_role == "admin"
    else:  # filtered
        return user_role in ["admin", "analyst", "manager"]
