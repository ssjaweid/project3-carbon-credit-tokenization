import streamlit as st

# Create a Streamlit web app
st.title("Car Consumption and Carbon Footprint Calculator")

# User inputs
car_type = st.selectbox("Select Car Type", ["Gas", "Hybrid", "Electric"])
miles_driven = st.number_input("Miles Driven", min_value=0, value=5000)
fuel_efficiency = st.number_input("Fuel Efficiency (mpg or eMPG)", min_value=0, value=6)

# Function to calculate emissions factor (in kg CO2e per mile)
def calculate_emissions_factor(miles_traveled, emissions_factor_per_mile):
    emissions_factor = (emissions_factor_per_mile / 1000) * miles_traveled
    return emissions_factor

# Input values for the emissions factor calculation (example values)
emissions_factor_per_mile = 0.42  # Emissions factor per mile (kg CO2e/mi)

# Calculate emissions factor
emissions_factor = calculate_emissions_factor(miles_driven, emissions_factor_per_mile)

# Calculate gas or energy consumption and carbon footprint based on car type
if car_type == "Electric":
    energy_consumption = miles_driven / fuel_efficiency
    st.write(f"Energy Consumption: {energy_consumption:.2f} kWh")

    # Calculate carbon emissions for electric cars in kgCO2e per mile using the emissions factor
    carbon_emissions = energy_consumption * emissions_factor

    st.write(f"Carbon Footprint: {carbon_emissions:.2f} kgCO2e")
    
    # Calculate carbon offset (assuming 100% renewable energy source)
    carbon_offset = carbon_emissions
    st.write(f"Carbon Offset: {carbon_offset:.2f} kgCO2e")

elif st.button("Calculate Now"):
    if car_type == "Gas":
        gas_consumption = miles_driven / fuel_efficiency
        st.write(f"Gas Consumption: {gas_consumption:.2f} gallons")

        # Average carbon emissions for gas cars in kgCO2e per mile
        carbon_emissions = gas_consumption * emissions_factor

        st.write(f"Carbon Footprint: {carbon_emissions:.2f} kgCO2e")

    elif car_type == "Hybrid":
        hybrid_consumption = miles_driven / fuel_efficiency
        st.write(f"Hybrid Consumption: {hybrid_consumption:.2f} gallons")

        # Average carbon emissions for hybrid cars in kgCO2e per mile
        carbon_emissions = hybrid_consumption * emissions_factor
        st.write(f"Carbon Footprint: {carbon_emissions:.2f} kgCO2e")

# Information about fuel efficiency and carbon emissions data source
st.info("Please note that the fuel efficiency and carbon emissions data should be based on real-world figures and specific to the car type you are using. You can obtain this data from trusted sources.")
