import streamlit as st
from PIL import Image

def custom_assets():
    



    logo_path = "assets/logo.png"
    logo = Image.open(logo_path)



    st.sidebar.image(logo, width=200)
        
    st.sidebar.markdown("""
    **Power of Data**  
    *O máximo de resultado em dados com o mínimo de tempo*
    📱 +55 11 96905.2103  
    🌐 www.powerofdata.ai
    """)
