import streamlit as st

pages = [
    st.Page(
        "pages/page1.py",
        title="Live Overview"
    ),
    st.Page(
        "pages/page2.py",
        title="Forecast Accuracy"
    ),
    st.Page(
        "pages/page3.py",
        title="Generation Mix"
    ),
    st.Page(
        "pages/page4.py",
        title="Smart Advisor"
    ),
]

st.navigation(pages).run()