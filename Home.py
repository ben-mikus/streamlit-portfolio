### Home.py
### The home page of my streamlit website as well as the main file from which it's deployed

import streamlit as st
import helper

st.set_page_config("Ben Mikus", layout="wide")

### HERO SECTION
col1, col2, col3, col4 = st.columns([2, 7.05, 1.95, 2], border=False)
### Left-aligned: Name, Title, Links
with col2:
    st.title("Ben Mikus")
    st.markdown("<p style='font-size:22px;'>Data Developer</p>", unsafe_allow_html=True)
    st.space()
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

### ABOUT SECTION
col1, col2, col3 = st.columns([2, 9, 2], border=False)

with col2:
    st.divider()
    st.space("small")
    st.markdown("Data Developer and Data Science graduate student. Working at the intersection of data, "
     "systems, and decision-making, I enjoy structuring raw data into meaningful forms. From cleaning and preprocessing "
     "to building data workflows, I see strong data foundations as the basis for reliable analysis. Furthermore, I take "
     "pride in translating numbers into insights that support decision-making and research, and I enjoy building visual "
     "tools that make complex patterns understandable and explorable.", text_alignment="justify")
    st.space("xxsmall")
    st.divider()

### PROJECTS SECTION
col1, col2, col3 = st.columns([2, 9, 2], border=False)

with col2:
    st.subheader("My Projects")
    "Chek out some of my recent work."
    st.space()

    col1, col2, col3 = st.columns([3, 3, 3])

    with col1:
        helper.project_card(title="Transaction Data Processor Demo",
                            description="Processing Engine",
                            image="media/project_one_cover.png",
                            link="https://benmikus.streamlit.app/~/+/Transaction_Data_Processor")



