
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
st.title("Conclusions")

st.text("""Through Snowflake’s unified data ecosystem and Streamlit’s interactivity, we’ve shown how aviation can analyze, act, and engage — all through data""")
st.markdown("""Net zero isn’t a **dream** — it’s a data problem we can solve byte by byte")