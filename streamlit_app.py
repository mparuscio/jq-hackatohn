
import streamlit as st
from snowflake.snowpark.context import get_active_session
import pydeck as pdk
import pandas as pd
import json
from snowflake.snowpark.functions import avg
import datetime
import altair as alt
import plotly.graph_objects as go



pg = st.navigation([
    st.Page("who.py", title="Who Are We"),
    st.Page("home.py", title="Introduction"),
    st.Page("architecture.py", title="Architecture"),
    st.Page("page1.py", title="Route Analysis"), 
    st.Page("page2.py", title="Overall"),
    st.Page("page3.py", title="Loyalty"),
    st.Page("page4.py", title="Seasonality"),
    st.Page("page5.py", title="Daily Variability"),
    st.Page("page6.py", title="Forecasts"),
    st.Page("proj.py", title="Project and Technologies")
],                   
    position="top")
pg.run()


