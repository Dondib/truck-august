
import pandas as pd
import streamlit as st
import plotly.express as px

# ===============================
# Streamlit App Configuration
# ===============================
st.set_page_config(
    page_title="Truck Logistics Dashboard",
    layout="wide",
    page_icon="🚛"
)

st.markdown(
    """
    <style>
        .main {
            background-color: #1e1e2f;
            color: #e0e0ff;
        }
        h1, h2, h3 {
            color: #bb86fc !important;
        }
        .stDataFrame, .stTable {
            background-color: #2b2b3d;
            border-radius: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ===============================
# Upload Excel File
# ===============================
st.title("🚛 Truck Logistics Dashboard - August 2025")

uploaded_file = st.file_uploader("📂 Upload your truck Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # ===============================
    # Filters
    # ===============================
    with st.sidebar:
        st.header("🔎 Filters")
        driver_filter = st.multiselect("Driver Name", df["Driver Name"].unique())
        product_filter = st.multiselect("Product", df["Product"].unique())
        destination_filter = st.multiselect("Destination", df["Destination"].unique())

    # Apply filters
    filtered_df = df.copy()
    if driver_filter:
        filtered_df = filtered_df[filtered_df["Driver Name"].isin(driver_filter)]
    if product_filter:
        filtered_df = filtered_df[filtered_df["Product"].isin(product_filter)]
    if destination_filter:
        filtered_df = filtered_df[filtered_df["Destination"].isin(destination_filter)]

    # ===============================
    # KPI Cards
    # ===============================
    st.subheader("📊 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Distance (km)", f"{filtered_df['Distance (km)'].sum():,.0f}")
    with col2:
        st.metric("Total Fuel Used (L)", f"{filtered_df['Fuel Used (liters)'].sum():,.0f}")
    with col3:
        st.metric("Total Net Weight (kg)", f"{filtered_df['Net Weight (kg)'].sum():,.0f}")
    with col4:
        st.metric("Total Trips", f"{len(filtered_df)}")

    # ===============================
    # Charts
    # ===============================
    st.subheader("📈 Analytics Charts")

    chart1 = px.bar(
        filtered_df,
        x="Driver Name",
        y="Distance (km)",
        color="Product",
        title="Distance by Driver & Product",
        text="Distance (km)"
    )
    chart1.update_layout(plot_bgcolor="#2b2b3d", paper_bgcolor="#1e1e2f", font=dict(color="white"))

    chart2 = px.pie(
        filtered_df,
        names="Product",
        values="Net Weight (kg)",
        title="Weight Distribution by Product"
    )
    chart2.update_layout(plot_bgcolor="#2b2b3d", paper_bgcolor="#1e1e2f", font=dict(color="white"))

    chart3 = px.line(
        filtered_df,
        x="Date",
        y="Fuel Used (liters)",
        color="Driver Name",
        title="Fuel Consumption Over Time",
        markers=True
    )
    chart3.update_layout(plot_bgcolor="#2b2b3d", paper_bgcolor="#1e1e2f", font=dict(color="white"))

    colA, colB = st.columns(2)
    with colA:
        st.plotly_chart(chart1, use_container_width=True)
    with colB:
        st.plotly_chart(chart2, use_container_width=True)

    st.plotly_chart(chart3, use_container_width=True)

    # ===============================
    # Data Table
    # ===============================
    st.subheader("📄 Detailed Trip Data")
    st.dataframe(filtered_df, use_container_width=True)

else:
    st.info("👆 Please upload your Excel file to view the dashboard.")
