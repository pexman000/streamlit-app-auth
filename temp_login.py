# Essayer plusieurs formats jusqu'à ce qu'un fonctionne
try:
    # Format 1 : deux arguments positionnels (certaines versions)
    name, authentication_status, username = authenticator.login('Connexion', 'main')
except (TypeError, ValueError) as e:
    try:
        # Format 2 : location='main' (nouvelles versions)
        authenticator.login(location='main')
        name = st.session_state.get('name')
        authentication_status = st.session_state.get('authentication_status')
        username = st.session_state.get('username')
    except Exception as e2:
        st.error(f"❌ Erreur : {e2}")
        name = None
        authentication_status = None
        username = None
