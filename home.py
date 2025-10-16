import streamlit as st


st.set_page_config(layout="wide")
st.title("Setting the Scene:  Problem Statement")
st.image("net_zero_byte_2.jpg")


st.text("How can data help us understand where to act, measure impact, and even engage customers to be part of the solution?")

st.markdown("""
The plan is formed by the following Three Pillars:
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


st.title("Approach")

st.markdown("""We built a data-driven sustainability simulation using Snowflake and Streamlit — to identify the key levers that can accelerate aviation toward net zero.
 \n
Attributes analyzed:
1. Use of Sustainable Aviation Fuel (SAF) – replacing fossil jet fuel.
2. Carbon Offsetting – investing in reforestation and renewable projects.
3. Green Membership Program – rewarding customers with points for eco-friendly choices, redeemable toward carbon offsets.
 \n
All this powered by dummy but realistic data representing airline operations and customer activity.""")

