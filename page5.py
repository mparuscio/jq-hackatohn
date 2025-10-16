
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
st.title("Daily Variability")

session = get_active_session()

db = "JETSTAR_SNOWCAMP_MOCK_DATA"
schema = "usecase_sustainability"

st.image("qantas_plan.png")



# Define the options for the dropdown
options = {
    "None" : 1, 
    "Payload (kg)" : "sum(PAYLOAD_KG)", 
    "Payload + Fuel (kg)" : "(sum(PAYLOAD_KG) + sum(FUEL_KG))",
    "Number of Filghts" : "COUNT(FB.FLIGHT_LEG_ID)",
    "Taxi Out (min)" : "(sum(TAXI_OUT_MIN))",
    "Wind" : "sum(WINDS_COMPONENT)",
    "Number of Filghts & Payload": "(sum(PAYLOAD_KG)*COUNT(FB.FLIGHT_LEG_ID))"
    }

# Create the selectbox
normalization_factor = st.selectbox(
    "Normalization Factor",
    options.keys()
)


normalized_seasonality_query =f"""
select sum(fuel_kg)/{options[normalization_factor]} fuel, hour(dep_ts) as hour, 
from {db}.{schema}.fuel_burn fb
full join {db}.{schema}.flight_schedule as fs on fs.flight_leg_id=fb.flight_leg_id 
full join {db}.{schema}.route_efficiency using(origin, destination)

group by hour
order by hour;
"""
normalized_seasonality_df = session.sql(normalized_seasonality_query).to_pandas()



# Create visualization
fig = go.Figure()


# Add line for total fuel
fig.add_trace(go.Scatter(
    name=f'Seasonality',
    x=normalized_seasonality_df["HOUR"],
    y=normalized_seasonality_df["FUEL"],
    mode='lines',
))
    

fig.update_layout(
    title='Normalized Overall Fuel Consumption by Hour',
    xaxis_title='Hour of Day',
    yaxis_title='Fuel Amount (kg)' if normalization_factor is "None" else f'Fuel Amount (kg)/{normalization_factor}',
)

st.plotly_chart(fig)

