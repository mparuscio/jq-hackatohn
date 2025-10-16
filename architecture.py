import streamlit as st


st.set_page_config(layout="wide")
st.title("Architecture")
st.image("Architecture.png")

st.markdown("""
Aviation is an **Hard-to-abate** sector, which means that we there are no short term plans to remove carbon-based fuels from the aircraft because such technology simply does not exist yet.
Despite this fact, the Qantas Group has a plan to reduce emissions and reach the **Net-0** by 2050! 
\n This plan is formed by the following Three Pillars:
""")

col1, col2, col3 = st.columns([1,1,1])

with col1:
    st.subheader("PILLAR ONE: **OPERATIONAL AND FLEET EFFICIENCY**")
    st.markdown("""
- Electrification of our
ground transport fleet
- Continuing to develop tools that
enable behavioural change and
greater operational efficiency
- Promoting Green tier among our
employees to encourage sustainable
behaviour at work, through their
commute and at home
""")
with col2:
    st.subheader("PILLAR TWO: **SUSTAINABLE AVIATION FUELS**")
    st.markdown("""
- Stimulating demand
- Increasing domestic production capability
- Increasing domestic feedstock availability
- Sending a strong demand signal to biofuel producers
""")
with col3:
    st.subheader("PILLAR THREE: **OFFSETTING**")
    st.markdown("""
- Fly Carbon Neutral
- Qantas Future Planet
- Australia Post Partnership
""")



