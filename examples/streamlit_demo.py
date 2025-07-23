"""
streamlit_demo.py

🚨 DEMO VISUELLE UNIQUEMENT 🚨

Ce script Streamlit est fourni à titre de démonstration rapide pour visualiser les données extraites
via le SDK DSP2 (identité, comptes, soldes, transactions).

Utilisez-le pour explorer visuellement le fonctionnement du SDK

Lancez avec :
    streamlit run examples/streamlit_demo.py
"""

import streamlit as st
from dsp2_client.core.client import DSP2Client
from streamlit_extras.let_it_rain import rain

# --- UI setup ---
st.set_page_config(page_title="DSP2 SDK Demo", layout="wide")
st.markdown("""
    <style>
    .stButton>button {background-color: #4F8BF9; color: white; font-weight: bold;}
    .stMarkdown {font-size: 1.1em;}
    </style>
""", unsafe_allow_html=True)
st.title("✨ DSP2 Client SDK — Visual Demo")

# --- Credentials input ---
with st.container():
    col1, col2 = st.columns([1,1])
    with col1:
        username = st.text_input("Username", value="mdupuis")
    with col2:
        password = st.text_input("Password", type="password", value="111111")

# --- Main action ---
if st.button("Afficher mes comptes et transactions 🚀"):
    try:
        with DSP2Client(username=username, password=password) as client:
            identity = client.get_identity()
            st.success("Authentification réussie !")
            rain(emoji="💸", font_size=25, falling_speed=5, animation_length="infinite")
            st.header("👤 Identité")
            st.json(identity.model_dump())

            accounts = client.list_accounts()
            for acc in accounts:
                st.divider()
                st.subheader(f"🏦 Compte : {acc.name or acc.id} ({acc.type})")
                st.json(acc.model_dump())
                balances = client.list_balances(acc.id)
                st.markdown("**💰 Balances**")
                st.json([bal.model_dump() for bal in balances])

                # Pagination dynamique sur les transactions :
                nb_tx = st.number_input(
                    f"Nombre de transactions à afficher pour ce compte ({acc.name or acc.id})",
                    min_value=1, max_value=50, value=10, key=f"tx_{acc.id}"
                )
                transactions = client.list_transactions(acc.id, page=1, count=int(nb_tx))
                st.markdown("**🧾 Transactions**")
                st.json([t.model_dump() for t in transactions])

    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")

else:
    st.info("Entrez vos identifiants et cliquez sur le bouton pour afficher vos comptes.")
