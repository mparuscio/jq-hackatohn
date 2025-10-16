
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
st.title("Route Analysis")

session = get_active_session()

db = "RAW"
schema = "analytics"

airport_coords = {
    "BNE" : [	-27.383333,	153.118332],
    "SYD" : [-33.947346,	151.179428],
    "MEL" : [-37.663712,	144.844788],
    "ADL": [-34.945,	138.531],
    "PER": [-31.940,	115.967]
    
}

au_pop_df = session.sql("Select lat, lng, population_proper as population from raw.map.au_population ").to_pandas()

population_layer = pdk.Layer(type='ColumnLayer',
                  data=au_pop_df,
                  get_position=['LNG', 'LAT'],
                  get_elevation='POPULATION',
                  auto_highlight=True,
                  elevation_scale=0.2,
                  pickable=True,
                  get_fill_color=['popl_div_100', 220],
                  coverage=6)


efficiency_query =f"""
select * from {db}.{schema}.origin_destination_summary_vw;
"""
efficiency_df = session.sql(efficiency_query).to_pandas()

# Route selection
selected_routes = st.multiselect(
    "Select Routes to Display",
    options=efficiency_df['ROUTE'].unique(),
    default=efficiency_df['ROUTE'].unique()
)

flights_query = f"""
select *
from {db}.{schema}.fuel_efficiency_vw;
"""
flights_df = session.sql(flights_query).to_pandas()
filtered_flights_df = flights_df[flights_df['ROUTE'].isin(selected_routes)]

filtered_flights_df["START_LAT"] = filtered_flights_df['ORIGIN'].map(lambda x: airport_coords[x][0])
filtered_flights_df["START_LON"] = filtered_flights_df['ORIGIN'].map(lambda x: airport_coords[x][1])
filtered_flights_df["END_LAT"] = filtered_flights_df['DESTINATION'].map(lambda x: airport_coords[x][0])
filtered_flights_df["END_LON"] = filtered_flights_df['DESTINATION'].map(lambda x: airport_coords[x][1])

layer = pdk.Layer(
    "LineLayer",
    data=filtered_flights_df,
    get_source_position='[START_LON, START_LAT]',
    get_target_position='[END_LON, END_LAT]',
    get_width=4,
    get_color=[0,0,1000],
    picking_radius=10,
    auto_highlight=True,
)


layers = [
    layer, 
    population_layer
]

view_state = pdk.ViewState(
    latitude=-23.8801299,
    longitude=133.8801299,
    zoom=3,
    pitch=40,
)

st.pydeck_chart(pdk.Deck(
    map_style=None,  # Use Streamlit theme to pick map style
    layers=layers,
    initial_view_state=view_state,
))



# Filter dataframe based on selected routes
filtered_df = efficiency_df[efficiency_df['ROUTE'].isin(selected_routes)]

# Create parameters per route
st.sidebar.header("Growth Rate Projections")
route_parameters = {}

for route in selected_routes:
    st.sidebar.subheader(f"Parameters for {route}")
    route_parameters[route] = {
        'initial_offset': st.sidebar.number_input(
            f"Initial Total Fuel Offset (kg) - {route}",
            value=0.,
            step=1e6,
            key=f"offset_{route}"
        ),
        'offset_fuel_growth': st.sidebar.slider(
            f"Offset Fuel Percentage Annual Growth (%) - {route}",
            0.0, 20.0, 1.0,
            key=f"offset__growth{route}"
        ),
        'total_fuel_growth': st.sidebar.slider(
            f"Total Fuel Annual Growth Rate (%) - {route}", 
            -10.0, 10.0, 2.0,
            key=f"total_fuel_{route}"
        ),
        'sustainable_fuel_growth': st.sidebar.slider(
            f"Sustainable Fuel Percentage Annual Growth (%) - {route}", 
            0.0, 20.0, 5.0,
            key=f"sust_fuel_{route}"
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
        offset_fuel = (row['OFFSET_FUEL_KG'] if row['OFFSET_FUEL_KG'] else  params['initial_offset']) * ((1+offset_percentage/100)** year) 
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

for index, row in filtered_df.iterrows():
    route = row['ROUTE']
    projections = calculate_projections(row, years_to_project, route_parameters[route])
    
    # Add line for total fuel
    fig.add_trace(go.Scatter(
        name=f'Total Fuel - {route}',
        x=[p['Year'] for p in projections],
        y=[p['Total Fuel'] for p in projections],
        mode='lines+markers',
        line=dict(width=3)
    ))
    
    # Add stacked bars for SAF components
    base = None  # This will store the base for stacking
    for offset_type in offset_types:
        fig.add_trace(go.Bar(
            name=f'{offset_type} - {route}',
            x=[p['Year'] for p in projections],
            y=[p['Sustainable Fuel'][offset_type] for p in projections],
            opacity=0.7,
                        base=base,  # Use the previous total as base
            offsetgroup=route  # This groups bars by route
                ))
            # Update base for next component
        if base is None:
            base = [p['Sustainable Fuel'][offset_type] for p in projections]
        else:
            base = [base[i] + p['Sustainable Fuel'][offset_type] for i, p in enumerate(projections)]


fig.update_layout(
    title='Fuel Consumption Projections by Route',
    xaxis_title='Year',
    yaxis_title='Fuel Amount (kg)',
    barmode='stack',
    showlegend=True
)

st.plotly_chart(fig)
