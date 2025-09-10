import pandas as pd
import streamlit as st

# Load your Excel data
df = pd.read_excel("truck_data_august.xlsx")

st.set_page_config(page_title="Truck Dashboard - August 2025", layout="wide")

st.title("🚛 Truck Dashboard - August 2025")

# Filters
col1, col2, col3 = st.columns(3)
with col1:
    truck = st.selectbox("Select Truck Plate", ["All"] + df["Truck Plate"].unique().tolist())
with col2:
    driver = st.selectbox("Select Driver", ["All"] + df["Driver Name"].unique().tolist())
with col3:
    product = st.selectbox("Select Product", ["All"] + df["Product"].unique().tolist())

# Apply filters
filtered_df = df.copy()
if truck != "All":
    filtered_df = filtered_df[filtered_df["Truck Plate"] == truck]
if driver != "All":
    filtered_df = filtered_df[filtered_df["Driver Name"] == driver]
if product != "All":
    filtered_df = filtered_df[filtered_df["Product"] == product]

st.subheader("Filtered Data")
st.dataframe(filtered_df)

# KPIs
total_distance = filtered_df["Distance (km)"].sum()
total_fuel = filtered_df["Fuel Used (liters)"].sum()
avg_efficiency = filtered_df["Fuel Efficiency (km/l)"].mean()

st.metric("Total Distance (km)", f"{total_distance:,.0f}")
st.metric("Total Fuel Used (liters)", f"{total_fuel:,.0f}")
st.metric("Average Fuel Efficiency (km/l)", f"{avg_efficiency:.2f}")
