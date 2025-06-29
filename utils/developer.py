import streamlit as st

def rodape_desenvolvedor():
    st.write("---")
    st.markdown("""
    <br>
    <div style='text-align: center; color: #666; font-size: 0.95em; margin-top:2em;'>
        <span style="color:#3064AD;font-weight:700;">Desenvolvido por</span> &nbsp;|&nbsp;
        <a href="https://www.linkedin.com/in/falkzera/" target="_blank" title="Ver LinkedIn de Lucas Falcão" style="color: #3064AD; font-weight:700; text-decoration: underline;">
            Lucas Falcão
        </a>
    </div>
    """, unsafe_allow_html=True)