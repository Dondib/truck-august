# app.py
import pandas as pd
import dash
from dash import dcc, html, dash_table, Input, Output
import plotly.express as px

# ---------- Load Excel ----------
FILE = "August_2025_Truck_Trips.xlsx"  # make sure this file is in the same folder
df = pd.read_excel(FILE)

# Ensure total weight exists (column name in your file: "Total Weight (kg)")
if "Total Weight (kg)" not in df.columns:
    df["Total Weight (kg)"] = df["Net Weight (kg)"] + df["Truck Weight (kg)"]

# ---------- Dash app ----------
app = dash.Dash(__name__)
server = app.server  # <-- for gunicorn / render

# Colors
BG = "#1e1e2f"
CARD = "#2d2d3f"
ACCENT = "#BB86FC"
TEXT = "#FFFFFF"

# Layout
app.layout = html.Div(style={'backgroundColor': BG, 'color': TEXT, 'padding': 20}, children=[
    html.H1("🚛 Truck Logistics Dashboard - August 2025", style={'textAlign': 'center', 'color': ACCENT}),

    # KPI Cards
    html.Div(style={'display': 'flex', 'gap': 20, 'marginTop': 20, 'marginBottom': 20}, children=[
        html.Div([
            html.Div("Total Distance (km)", style={'color': ACCENT}),
            html.H3(id='kpi-distance')
        ], style={'backgroundColor': CARD, 'padding': 16, 'borderRadius': 10, 'flex': 1, 'textAlign': 'center'}),

        html.Div([
            html.Div("Total Fuel (L)", style={'color': ACCENT}),
            html.H3(id='kpi-fuel')
        ], style={'backgroundColor': CARD, 'padding': 16, 'borderRadius': 10, 'flex': 1, 'textAlign': 'center'}),

        html.Div([
            html.Div("Avg Efficiency (km/L)", style={'color': ACCENT}),
            html.H3(id='kpi-eff')
        ], style={'backgroundColor': CARD, 'padding': 16, 'borderRadius': 10, 'flex': 1, 'textAlign': 'center'}),
    ]),

    # Filters row
    html.Div(style={'display': 'flex', 'gap': 20, 'marginBottom': 10}, children=[
        html.Div([
            html.Label("Driver", style={'color': ACCENT}),
            dcc.Dropdown(
                id='driver-filter',
                options=[{'label': d, 'value': d} for d in sorted(df['Driver Name'].unique())],
                multi=True,
                placeholder='Filter by driver'
            )
        ], style={'flex': 1}),

        html.Div([
            html.Label("Product", style={'color': ACCENT}),
            dcc.Dropdown(
                id='product-filter',
                options=[{'label': p, 'value': p} for p in sorted(df['Product'].unique())],
                multi=True,
                placeholder='Filter by product'
            )
        ], style={'flex': 1}),

        html.Div([
            html.Label(" ", style={'color': ACCENT}),
            html.Button("⬇️ Download Excel (filtered)", id='btn-download', style={'width': '100%', 'padding': '10px', 'backgroundColor': '#8E44AD', 'color': 'white', 'border': 'none', 'borderRadius': 6})
        ], style={'width': 220})
    ]),

    # Chart
    dcc.Graph(id='distance-chart'),

    # Table
    html.H3("📋 Trip Details", style={'color': ACCENT, 'marginTop': 20}),
    dash_table.DataTable(
        id='trip-table',
        columns=[{"name": c, "id": c} for c in df.columns],
        page_size=10,
        style_table={'overflowX': 'auto'},
        style_cell={'backgroundColor': CARD, 'color': TEXT, 'textAlign': 'center', 'padding': '6px'},
        style_header={'backgroundColor': ACCENT, 'color': 'black', 'fontWeight': 'bold'},
        style_data_conditional=[{'if': {'row_index': 'odd'}, 'backgroundColor': '#333445'}]
    ),
    dcc.Download(id="download-dataframe-xlsx")
])


# ---------- Callbacks ----------
@app.callback(
    [Output('distance-chart', 'figure'),
     Output('trip-table', 'data'),
     Output('kpi-distance', 'children'),
     Output('kpi-fuel', 'children'),
     Output('kpi-eff', 'children')],
    [Input('driver-filter', 'value'),
     Input('product-filter', 'value')]
)
def update_ui(selected_drivers, selected_products):
    dff = df.copy()
    if selected_drivers:
        dff = dff[dff['Driver Name'].isin(selected_drivers)]
    if selected_products:
        dff = dff[dff['Product'].isin(selected_products)]

    # Chart
    fig = px.bar(
        dff,
        x="Date",
        y="Distance (km)",
        color="Driver Name",
        barmode="group",
        title="Distance per Trip",
        template='plotly_dark'
    )
    fig.update_layout(plot_bgcolor=BG, paper_bgcolor=BG, font_color=TEXT)

    # KPIs
    total_distance = f"{dff['Distance (km)'].sum():,.0f}"
    total_fuel = f"{dff['Fuel Used (liters)'].sum():,.0f}"
    avg_eff = f"{dff['Fuel Efficiency (km/l)'].mean():.2f}" if not dff.empty else "0.00"

    return fig, dff.to_dict('records'), total_distance, total_fuel, avg_eff


@app.callback(
    Output("download-dataframe-xlsx", "data"),
    Input("btn-download", "n_clicks"),
    Input('driver-filter', 'value'),
    Input('product-filter', 'value'),
    prevent_initial_call=True,
)
def download_filtered(n_clicks, selected_drivers, selected_products):
    dff = df.copy()
    if selected_drivers:
        dff = dff[dff['Driver Name'].isin(selected_drivers)]
    if selected_products:
        dff = dff[dff['Product'].isin(selected_products)]

    return dcc.send_data_frame(dff.to_excel, "Filtered_Truck_Trips_August2025.xlsx", index=False)


# ---------- Run (for local dev) ----------
if __name__ == "__main__":
    app.run(debug=True)
