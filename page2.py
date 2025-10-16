
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
st.title("Overall")

session = get_active_session()

db = "RAW"
schema = "ANALYTICS"

st.image("qantas_plan.png")


efficiency_query =f"""
select * from {db}.{schema}.origin_destination_summary_vw;
"""
efficiency_df = session.sql(efficiency_query).to_pandas()


# Create parameters per route
st.sidebar.header("Growth Rate Projections")
route_parameters = {}

st.sidebar.subheader(f"Overall Parameters")
overall_parameters = {
    'offset_fuel_growth': st.sidebar.slider(
        f"Offset Fuel Percentage Annual Growth (%)",
        0.0, 20.0, 1.0,
        key=f"offset__growth"
    ),
    'total_fuel_growth': st.sidebar.slider(
        f"Total Fuel Annual Growth Rate (%)", 
        -10.0, 10.0, 2.0,
        key=f"total_fuel_"
    ),
    'sustainable_fuel_growth': st.sidebar.slider(
        f"Sustainable Fuel Percentage Annual Growth (%)", 
        0.0, 20.0, 5.0,
        key=f"sust_fuel_"
    )
}

years_to_project = 25

offset_types = ["OFFSET", "SAF"]





# Calculate projections for each route
def calculate_projections(row, years, params):
    projections = []
    for year in range(years + 1):
        total_fuel = (row['TOTAL_FUEL_KG']) * (1 + params['total_fuel_growth']/100) ** year
        sust_percentage = params['sustainable_fuel_growth']
        sustainable_fuel = row['SAF'] * ((1+ sust_percentage/100)**year)
        offset_percentage = params['offset_fuel_growth'] 
        offset_fuel = (row['OFFSET_FUEL_KG']) * ((1+offset_percentage/100)** year) 
        # Calculate individual SAF components using the df dataframe
        saf_components = {}
        # for saf_type in offset_type:  # Assuming df has saf_type column
        #     component_pct = df[df['saf_type'] == saf_type]['percentage'].iloc[0]  # Get percentage for this SAF type
        #     saf_components[saf_type] = sustainable_fuel * (component_pct/100)
        saf_components = { "SAF" : sustainable_fuel, "OFFSET" : offset_fuel}
        projections.append({
            'Year': f'{ 2025 + year}',
            'Total Fuel': total_fuel,
            'Sustainable Fuel': saf_components
        })
    return projections

# Create visualization
fig = go.Figure()

for index, row in efficiency_df.iterrows():
    projections = calculate_projections(row, years_to_project, overall_parameters)
    
    # Add line for total fuel
    fig.add_trace(go.Scatter(
        name=f'Total Fuel',
        x=[p['Year'] for p in projections],
        y=[p['Total Fuel'] for p in projections],
        mode='lines+markers',
        line=dict(width=3)
    ))
    
    # Add stacked bars for SAF components
    base = None  # This will store the base for stacking
    for offset_type in offset_types:
        fig.add_trace(go.Bar(
            name=f'{offset_type}',
            x=[p['Year'] for p in projections],
            y=[p['Sustainable Fuel'][offset_type] for p in projections],
            opacity=0.7,
            base=base, 
        ))
        if base is None:
            base = [p['Sustainable Fuel'][offset_type] for p in projections]
        else:
            base = [base[i] + p['Sustainable Fuel'][offset_type] for i, p in enumerate(projections)]


fig.update_layout(
    title='Overall Fuel Consumption Projections',
    xaxis_title='Year',
    yaxis_title='Fuel Amount (kg)',
    barmode='stack',
    showlegend=True
)

st.plotly_chart(fig)
