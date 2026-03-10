### Home.py
### The home page of my streamlit website as well as the main file from which it's deployed

import streamlit as st
import helper

st.set_page_config("Ben Mikus", layout="wide")

### HERO SECTION
col1, col2, col3, col4 = st.columns([2, 7.5, 1.5, 2], border=False)
### Left-aligned: Name, Title, Links
with col2:
    st.title("Ben Mikus")
    st.markdown("<p style='font-size:22px;'>Data Science Graduate Student</p>", unsafe_allow_html=True)
    st.markdown("""
        <div style="display:flex; gap:10px; flex-wrap:wrap;">
            <a href="https://github.com/ben-mikus" target="_blank" style="text-decoration:none;">
                <span style="background:#ddd6fe; padding:3px 5px; border-radius:6px;font-size:14px;">GitHub</span>
            <a>
            <a href="https://linkedin.com/in/benmikus" target="_blank" style="text-decoration:none;">
                <span style="background:#bfdbfe; padding:3px 5px; border-radius:6px;font-size:14px;">LinkedIn</span>
            <a>
        </div>
        """, unsafe_allow_html=True)

### Right-aligned: profile picture
with col3:
    st.image("media/Profile.jpg", width=190)

### PROJECTS SECTION

col1, col2, col3 = st.columns([2, 9, 2], border=False)

with col2:

    st.space()
    st.divider()
    st.space()

    st.subheader("My Projects")
    "Chek out some of my recent work."
    st.space()

    col1, col2, col3 = st.columns([3, 3, 3])

    with col1:
        helper.project_card(title="Transaction Data Processor Demo",
                            description="Processing Engine",
                            image="media/project_one_cover.png",
                            link="https://benmikus.streamlit.app/~/+/Transaction_Data_Processor")



