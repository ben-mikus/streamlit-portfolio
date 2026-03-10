### helper.py
### Storage for helper functions that I use to build my website

import streamlit as st

def project_card(title, description, image, link):

    with st.container(border=True):

        st.subheader(f"{title}")

        st.badge(description, color="blue")

        st.image(image, width="stretch")

        st.link_button("View Project", url=link)

### header function to apply the header style I like
def header(text, size=20, bold=True):
    weight = "bold" if bold else "normal"
    st.markdown(
        f"<p style='font-size:{size}px; font-weight:{weight};'>{text}</p>",
        unsafe_allow_html=True
    )