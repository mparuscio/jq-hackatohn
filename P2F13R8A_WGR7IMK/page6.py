
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
st.title("Forecasts")

session = get_active_session()

# Create visualization
fig = go.Figure()
db = "SNOWCOMP_CUSTOM_DATA"
schema = "JETSTAR_SUSTAIN_SCHEMA"

query = f"""-- Union your predictions with your historical data, then view the results in a chart.
SELECT DEP_TS, FUEL_KG AS actual, NULL AS forecast, NULL AS lower_bound, NULL AS upper_bound
    FROM {db}.{schema}.NEW_TS
"""

nd = st.slider("Prediction Days", step=1, min_value=0, max_value=90)



df = session.sql(query).to_pandas()

forecast_df = session.sql(f"""SELECT ts as DEP_TS, NULL AS actual, forecast, lower_bound, upper_bound
    FROM {db}.{schema}.My_forecasts_2025_10_15 where DAYOFYEAR(DEP_TS)<= {nd}""").to_pandas()
# Add line for total fuel
fig.add_trace(go.Scatter(
    name=f'Data',
    x=df["DEP_TS"],
    y=df["ACTUAL"],
    mode='lines',
))
fig.add_trace(go.Scatter(
    name=f'Forecast UB',
    x=forecast_df["DEP_TS"],
    y=forecast_df["UPPER_BOUND"],
    mode='lines',
    line=dict(color='green', width=2)
)) 

fig.add_trace(go.Scatter(
    name=f'Forecast AVG',
    x=forecast_df["DEP_TS"],
    y=forecast_df["FORECAST"],
    mode='lines',
    line=dict(color='#FF0000', width=2)
))

fig.add_trace(go.Scatter(
    name=f'Forecast LB',
    x=forecast_df["DEP_TS"],
    y=forecast_df["LOWER_BOUND"],
    mode='lines',
    line=dict(color='orange', width=2)
))
    

fig.update_layout(
    title='Average Fuel Consumption per Day',
    xaxis_title='Date',
    yaxis_title='Fuel Amount (kg)',
)

st.plotly_chart(fig)