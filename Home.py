### Home.py
### The home page of my streamlit website as well as the main file from which it's deployed

import streamlit as st
import helper

st.set_page_config("Ben Mikus", layout="wide")

### HERO SECTION
col1, col2, col3, col4, col5, col6 = st.columns([2, 3, 3, 1.25, 1.7, 2], border=False)
### Left-aligned: Name, Title, Links
with col2:
    st.title("Ben Mikus")
    st.markdown("<p style='font-size:22px;'>Data Developer</p>", unsafe_allow_html=True)
    st.space()

    col1, col2, col3 = st.columns([0.15, 0.22, 0.73])
    with col1:
        st.image(
            "media/GitHub-Logo.png",
            width=30,
            link="https://github.com/ben-mikus"
        )
    with col2:
        st.image(
            "media/Linkedin-Logo.png",
            width=55,
            link="https://www.linkedin.com/in/benmikus/"
        )

### Right-aligned: profile picture
with col5:
    st.image("media/Profile.jpg", width=190)

### ABOUT SECTION
col1, col2, col3, col4 = st.columns([2, 9, 0.25, 2], border=False)

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
                            link='<a href="?page=1_Plotting_Demo">')



