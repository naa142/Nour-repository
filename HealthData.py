import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import geopy
from geopy.geocoders import Nominatim
import timepi

st.title("Health data in Lebanon")
# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
data=pd.read_csv(r"C:\Users\Nour Abd El Ghani\Downloads\4a0321bc971cc2f793d3367fd0b55a34_20240905_102823.csv")
#data
if st.checkbox('Show data'):
    st.write("Dataset Overview:")
    st.dataframe(data)
    
st.subheader("COVID-19 Cases by Area")



# Assuming the dataset has columns 'refArea' and 'Nb of Covid-19 cases'
if 'refArea' in data.columns and 'Nb of Covid-19 cases' in data.columns:
    
    # Sidebar: Select Area
    areas = data['refArea'].unique()
    selected_areas = st.sidebar.multiselect("Select Areas:", areas, default=areas)

    # Sidebar: Toggle between raw data and percentage
    show_percentage = st.sidebar.checkbox("Show as percentage of total cases", value=False)

    # Filter the dataset based on selected areas
    filtered_data = data[data['refArea'].isin(selected_areas)]

    # Adjust the y-axis if showing percentages
    if show_percentage:
        total_cases = filtered_data['Nb of Covid-19 cases'].sum()
        filtered_data['Nb of Covid-19 cases'] = (filtered_data['Nb of Covid-19 cases'] / total_cases) * 100

    # Bar Chart: COVID-19 Cases by Area
    fig_bar = px.bar(filtered_data, x='refArea', y='Nb of Covid-19 cases',
                     title="COVID-19 Cases by Area",
                     labels={'refArea': 'Area', 'Nb of Covid-19 cases': 'Number of Cases' if not show_percentage else 'Percentage of Cases'},
                     template='plotly_dark')
    
    # Pie Chart: Distribution of Cases by Area
    fig_pie = px.pie(filtered_data, values='Nb of Covid-19 cases', names='refArea',
                     title="COVID-19 Case Distribution by Area",
                     template='plotly_dark')

    # Layout adjustments for bar chart and pie chart
    fig_bar.update_layout(transition_duration=500)
    fig_pie.update_traces(textinfo='percent+label' if show_percentage else 'label')

    # Display the Bar Chart
    st.plotly_chart(fig_bar)

    # Display the Pie Chart
    st.plotly_chart(fig_pie)

    # Additional Metric: Display total number of cases for selected areas
    total_cases_selected = filtered_data['Nb of Covid-19 cases'].sum() if not show_percentage else 100
    st.write(f"Total cases in selected areas: **{total_cases_selected:.2f}**")

else:
    st.error("Columns 'refArea' or 'Nb of Covid-19 cases' not found in the dataset.")
    
from geopy.geocoders import Nominatim
import time
df = pd.DataFrame(data)
# Initialize Nominatim API for geocoding
geolocator = Nominatim(user_agent="geoapiExercises")

# Function to get latitude and longitude from area name
def get_lat_lon(area):
    try:
        location = geolocator.geocode(area)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except Exception as e:
        print(f"Error retrieving data for {area}: {e}")
        return None, None

# Create empty columns for latitude and longitude
df['lat'] = None
df['lon'] = None

# Get latitude and longitude for each area
for i, area in enumerate(df['refArea']):
    lat, lon = get_lat_lon(area)
    df.at[i, 'lat'] = lat
    df.at[i, 'lon'] = lon
    time.sleep(1)  # Sleep for 1 second to avoid hitting the geocoding rate limit
    

# Remove rows where lat or lon couldn't be retrieved
df = df.dropna(subset=['lat', 'lon'])

# Display the data with lat/lon
st.title('COVID-19 Cases Map with Geocoded Data')
st.write("Map of COVID-19 cases by area, represented by location.")
st.map(df[['lat', 'lon']])

# Show the updated DataFrame
st.write("Table showing COVID-19 cases by area with latitude and longitude:")
st.dataframe(df)