#  Truck Logistics Dashboard

An interactive analytics dashboard built with **Streamlit**, **Pandas**, and **Plotly**.  
It helps track truck trips, distances, fuel usage, and product deliveries from an Excel file.

---

##  Features
- Upload your **Excel file** with trip data (`.xlsx`)
- Filter by **Driver, Product, or Destination**
- View **Key Metrics**:
  - Total Distance (km)  
  - Total Fuel Used (L)  
  - Total Net Weight (kg)  
  - Total Trips
- Interactive **Charts**:
  - Distance by Driver & Product (Bar Chart)  
  - Product Weight Distribution (Pie Chart)  
  - Fuel Consumption Over Time (Line Chart)  
- Browse **detailed trip data** in a dynamic table

---

##  Deployment
This project runs on [Streamlit]().

### Run locally
```bash
# Clone the repo
git clone https://github.com/Dondib/truck-august.git
cd truck-august

# Install dependencies
pip install -r requirements.txt

# Start the dashboard
streamlit run app.py
https://truck-august-y7kdxggjp9plqqlivm3rwp.streamlit.app/


