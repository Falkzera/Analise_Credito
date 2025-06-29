import streamlit as st
from nbconvert import HTMLExporter
import nbformat

notebook_path = "notebook/Modelo.ipynb"

with open(notebook_path, "r", encoding="utf-8") as f:
    notebook_content = nbformat.read(f, as_version=4)

html_exporter = HTMLExporter()
(body, resources) = html_exporter.from_notebook_node(notebook_content)

with st.container(border=True):
    st.components.v1.html(body, height=800, scrolling=True)