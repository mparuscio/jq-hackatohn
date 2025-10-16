

import streamlit as st
from snowflake.snowpark.context import get_active_session
import pydeck as pdk
import pandas as pd
import json
from snowflake.snowpark.functions import avg
import datetime
import altair as alt
import plotly.graph_objects as go

st.set_page_config(layout="wide")

st.title("Loyalty")
st.write("""Our ‘tick-the-box’ to Fly Carbon Neutral offsetting program is one of the largest of any airline.
And since 2007, we have offset our own ground and corporate travel emissions.
As a hard-to-abate sector, carbon offsetting will remain a key lever in aviation’s global
transition to a low carbon economy and in helping the Qantas Group meet our commitments of
capping emissions at 2019 levels and reaching net zero emissions by 2050.
In 2019, we enabled Qantas Frequent Flyer members and Qantas Business Rewards
customers to earn 10 Qantas Points for every dollar spent on offsetting. Qantas matches
dollar-for-dollar every contribution a customer makes to offset their emissions on a passenger
flight, effectively doubling the size of the program.""")

session = get_active_session()

with_clause = """with base as (select * from raw.analytics.loyalty_members_vw)"""

generations_df = session.sql(f"""{with_clause} select sum(TREES_PLANTED_BY_QANTAS) as trees_count, count(distinct member_id) as num_member, trees_count/num_member as normalized_trees, GENERATION  
from base group by GENERATION""").to_pandas()

route_df = session.sql(f"""{with_clause} select concat(DEPARTURE, '->', ARRIVAL) as route,sum(TREES_PLANTED_BY_QANTAS) as trees_count, count(distinct member_id) as num_member, trees_count/num_member as normalized_trees  
from base group by route""").to_pandas()


st.header("Green Tier")
st.write("""Qantas was the first airline in the world to announce (in
November 2021) a recognition and rewards initiative, a new
**Green tier**, as part of its Frequent Flyer Program, designed to
encourage and recognise its members for making more
sustainable choices both in the air and on the ground.""")

st.image("green_tier_all.png")

# col1, col2 = st.columns([2,2])

# with col1:
#     st.image("achieve_green_tier.png", )

# with col2:
#     st.image("green_tier.png")

st.bar_chart(data=generations_df, x= 'GENERATION', y = 'TREES_COUNT',y_label="Trees Planted", x_label="Generation")
st.bar_chart(data=route_df, x= 'ROUTE', y = 'TREES_COUNT',y_label="Trees Planted", x_label="Route")