
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
st.title("Project and Technologies")

st.markdown("""
- Snowflake Data Sharing
- Snowflake Data Unload
- Snowflake dbt project
- Streamlit in Snowflake
- Snowflake Forecasts
""")