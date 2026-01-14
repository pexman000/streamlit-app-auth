# utils/audit.py
import logging
import os
from datetime import datetime
import streamlit as st

# Créer le dossier logs s'il n'existe pas
log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Configuration du logging
log_file = os.path.join(log_dir, 'audit.log')
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='a'  # Mode append pour ajouter au fichier existant
)


def log_action(action: str, details: str = ""):
    """Enregistre une action utilisateur"""
    username = st.session_state.get('username', 'anonymous')
    role = st.session_state.get('role', 'unknown')
    
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'username': username,
        'role': role,
        'action': action,
        'details': details
    }
    
    logging.info(f"USER={username} ROLE={role} ACTION={action} DETAILS={details}")
    
    return log_entry


def log_data_access(table: str, filters: dict = None):
    """Log l'accès aux données"""
    log_action(
        action="DATA_ACCESS",
        details=f"table={table} filters={filters}"
    )


def log_export(export_type: str, row_count: int):
    """Log les exports"""
    log_action(
        action="DATA_EXPORT",
        details=f"type={export_type} rows={row_count}"
    )


def log_modification(table: str, record_id: str, changes: dict):
    """Log les modifications"""
    log_action(
        action="DATA_MODIFY",
        details=f"table={table} id={record_id} changes={changes}"
    )


# Utilisation
# log_data_access("ventes", {"region": "Nord", "annee": 2024})
# log_export("csv", 1500)
# log_modification("clients", "CLI001", {"email": "nouveau@email.com"})
