# utils/permissions.py
"""
Module de gestion des permissions basées sur les rôles
"""
from enum import Enum
from typing import List
import streamlit as st


class Role(Enum):
    """Énumération des rôles disponibles"""
    ADMIN = "admin"
    ANALYST = "analyst"
    MANAGER = "manager"
    VIEWER = "viewer"


# Définition des permissions par rôle
ROLE_PERMISSIONS = {
    "admin": [
        "view_dashboard",
        "view_sensitive_data",
        "edit_data",
        "delete_data",
        "export_all",
        "manage_users",
        "view_all_data",
        "view_logs"
    ],
    "analyst": [
        "view_dashboard",
        "view_sensitive_data",
        "export_filtered",
        "view_department_data",
        "create_reports"
    ],
    "manager": [
        "view_dashboard",
        "view_sensitive_data",
        "edit_data",
        "export_filtered",
        "view_team_data",
        "approve_requests"
    ],
    "viewer": [
        "view_dashboard",
        "export_filtered"
    ]
}


def get_user_permissions(role: str) -> List[str]:
    """
    Retourne la liste des permissions pour un rôle donné
    
    Args:
        role: Le rôle de l'utilisateur (admin, analyst, manager, viewer)
        
    Returns:
        Liste des permissions associées au rôle
    """
    return ROLE_PERMISSIONS.get(role.lower(), [])


def has_permission(role: str, permission: str) -> bool:
    """
    Vérifie si un rôle possède une permission spécifique
    
    Args:
        role: Le rôle de l'utilisateur
        permission: La permission à vérifier
        
    Returns:
        True si le rôle possède la permission, False sinon
    """
    user_permissions = get_user_permissions(role)
    return permission in user_permissions


def require_permission(permission: str):
    """
    Décorateur pour protéger une fonction avec une permission
    
    Usage:
        @require_permission("edit_data")
        def ma_fonction():
            # Code protégé
            pass
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not st.session_state.get('authenticated', False):
                st.error("🚫 Vous devez être connecté")
                st.stop()
                
            user_role = st.session_state.get('role', 'viewer')
            if not has_permission(user_role, permission):
                st.error(f"🚫 Permission refusée : {permission}")
                st.stop()
                
            return func(*args, **kwargs)
        return wrapper
    return decorator
