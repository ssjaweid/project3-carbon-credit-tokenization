import streamlit as st
import pandas as pd
import math
import requests

# Function to calculate distance between cities using Google Maps API
def calculate_distance(from_city, to_city, api_key):
    base_url = 'https://maps.googleapis.com/maps/api/distancematrix/json'
    params = {
        'origins': from_city,
        'destinations': to_city,
        'key': api_key,
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    if data.get('status') == 'OK':
        try:
            distance_text = data['rows'][0]['elements'][0]['distance']['text']
            return distance_text
        except KeyError:
            return "Distance data not found"
    else:
        return "Invalid city name(s)"

# Function to calculate haversine distance
def haversine_distance(lat1, lon1, lat2, lon2):
    earth_radius = 3958.8
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = earth_radius * c
    return distance

# Create a Streamlit web app
st.title("Carbon Footprint Calculator")

# Car Calculator
st.subheader("Car Carbon Footprint Calculator")
car_type = st.radio("Select Car Type", ["Gas", "Hybrid", "Electric"])
miles_driven = st.number_input("Miles Driven", min_value=0, value=5000)
fuel_efficiency = st.number_input("Fuel Efficiency (mpg or eMPG)", min_value=0, value=6)

# Car Carbon Footprint Calculation
if st.button("Calculate Car Carbon Footprint"):
    emissions_factor_per_mile = 0.42  # Example emissions factor (kg CO2e per mile)
    emissions_factor_per_km = 0.621371 * emissions_factor_per_mile  # Convert to kg CO2e per km

    if car_type == "Electric":
        energy_consumption = miles_driven / fuel_efficiency

        carbon_emissions_miles = miles_driven * emissions_factor_per_mile
        carbon_emissions_km = energy_consumption * emissions_factor_per_km

        st.write(f"Energy Consumption: {energy_consumption:.2f} kWh")
        st.write(f"Carbon Footprint (Miles): {carbon_emissions_miles:.2f} kg CO2e")
        st.write(f"Carbon Footprint (Kilometers): {carbon_emissions_km:.2f} kg CO2e")

    elif car_type == "Gas" or car_type == "Hybrid":
        consumption = miles_driven / fuel_efficiency

        carbon_emissions_miles = miles_driven * emissions_factor_per_mile
        carbon_emissions_km = consumption * emissions_factor_per_km

        st.write(f"Fuel Consumption: {consumption:.2f} gallons")
        st.write(f"Carbon Footprint (Miles): {carbon_emissions_miles:.2f} kg CO2e")
        st.write(f"Carbon Footprint (Kilometers): {carbon_emissions_km:.2f} kg CO2e")

# Rail/Bus Calculator
st.subheader("Rail/Bus Carbon Footprint Calculator")
transportation_type = st.selectbox("Select transporation type", ["Rail", "Bus"])
from_city = st.text_input("From City", "")
to_city = st.text_input("To City", "")
google_api_key = 'AIzaSyCIx-_G27hwPK97r6B_b4FyF4sTxHq7qWw'
# Rail/Bus Carbon Footprint Calculation
if st.button("Calculate Rail/Bus Carbon Footprint"):
    api_key = 'AIzaSyCIx-_G27hwPK97r6B_b4FyF4sTxHq7qWw'
distance = calculate_distance(from_city, to_city, google_api_key)

if "Invalid" not in distance:
    distance_km = float(distance.split()[0])
    distance_miles = distance_km * 0.621371
    distance_text = calculate_distance(from_city, to_city, google_api_key)
    
    if transportation_type == "Rail":
            emissions_factor_per_mile = 0.46
            miles_traveled = float(distance_miles)
            trans_carbon = emissions_factor_per_mile * miles_traveled
            st.success(f"Carbon Footprint for Rail: {trans_carbon:.2f} kgCO2e")
    elif transportation_type == "Bus":
            emissions_factor_per_mile = 0.4
            miles_traveled = float(distance_miles)
            trans_carbon = emissions_factor_per_mile * miles_traveled
            st.success(f"Carbon Footprint for Bus: {trans_carbon:.2f} kgCO2e")

    st.write(f"Distance: {distance}")
    st.write(f"Carbon Footprint (Miles): {trans_carbon:.2f} kg CO2e")
else:
    st.error("Invalid city name(s)")

# Air Miles Calculator
st.subheader("Air Miles Carbon Footprint Calculator")
from_iata = st.text_input("From IATA Code", "").strip().upper()
to_iata = st.text_input("To IATA Code", "").strip().upper()

# Air Miles Carbon Footprint Calculation
if st.button("Calculate Air Miles Carbon Footprint"):
    airport_data = pd.read_csv('iata-icao.csv')

    lat1, lon1 = 40.7128, -74.0060
    lat2, lon2 = 34.0522, -118.2437  

    # Calculate the air miles distance
    distance = haversine_distance(lat1, lon1, lat2, lon2)
    st.write(f"Air miles distance: {distance:.2f} miles")

    # Look up coordinates for the provided IATA codes
    from_airport = airport_data[airport_data['iata'] == from_iata]
    to_airport = airport_data[airport_data['iata'] == to_iata]

    if not from_airport.empty and not to_airport.empty:
        lat1, lon1 = from_airport['latitude'].values[0], from_airport['longitude'].values[0]
        lat2, lon2 = to_airport['latitude'].values[0], to_airport['longitude'].values[0]

        distance = haversine_distance(lat1, lon1, lat2, lon2)
        emissions_factor = 1.47
        air_miles_carbon = distance * emissions_factor

        st.write(f"Flight Distance: {distance:.2f} miles")
        st.write(f"Carbon Footprint (Miles): {air_miles_carbon:.2f} kg CO2e")
    else:
        st.error("Invalid IATA codes. Please provide valid IATA codes")