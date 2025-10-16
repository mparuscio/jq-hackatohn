import streamlit as st


st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center;'>Team 5 - Net Zero Bytes</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Sustainability & Carbon Footprint</h1>", unsafe_allow_html=True)
st.image("bg.png")
col1, col2, col3, col4 = st.columns([1,1,1,1])

with col1:
    st.text("Mayur Sankhe")


with col2:
    st.text("Marco Paruscio")


with col3:
    st.text("Ashutosh Uniyal")


with col4:
    st.text("Keyvan Jaferzadeh Khorramabadian")



