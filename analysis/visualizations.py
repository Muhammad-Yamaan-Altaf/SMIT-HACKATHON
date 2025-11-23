# analysis/visualizations.py (FINAL - Gauge Chart Sizing Fix)

from typing import Any, Dict

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import html
import dash_bootstrap_components as dbc 

# --- create_mock_history function (No change) ---
def create_mock_history(df: pd.DataFrame) -> pd.DataFrame:
    if len(df) > 1: return df
    current_time = df.index[0]
    current_temp = df['Temperature_C'].iloc[0]
    city_name = df['City'].iloc[0]
    mock_temps = []
    mock_times = []
    for hour in range(3, 0, -1):
        mock_time = current_time - pd.Timedelta(hours=hour)
        mock_temp = current_temp + np.random.uniform(-1.5, 1.5)
        mock_times.append(mock_time)
        mock_temps.append(mock_temp)
    mock_df = pd.DataFrame({
        'Timestamp': mock_times + [current_time],
        'Temperature_C': mock_temps + [current_temp],
        'City': city_name
    }).set_index('Timestamp')
    for col in df.columns:
        if col not in mock_df.columns:
            mock_df[col] = df[col].iloc[0]
    return mock_df.sort_index()

# --- create_temperature_chart function (No change) ---
def create_temperature_chart(df: pd.DataFrame) -> Dict[str, Any]:
    if df.empty or 'Temperature_C' not in df.columns:
        return {}
    df = create_mock_history(df)
    df = df.reset_index()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['Timestamp'], 
        y=df['Temperature_C'], 
        mode='lines+markers',
        line=dict(shape='spline', color='#10b981', width=3),
        fill='tozeroy', 
        fillcolor='rgba(16, 185, 129, 0.2)',
        marker=dict(size=8, color='#10b981', line=dict(width=1, color='White')),
        name='Temperature'
    ))
    fig.update_layout(
        title=f"Temperature Trend in {df['City'].iloc[0]} (°C)",
        xaxis_title="Time", 
        yaxis_title="Temperature (°C)",
        title_x=0.5,
        template="plotly_dark", 
        hovermode="x unified",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=400,
        margin=dict(l=40, r=20, t=50, b=40)
    )
    return fig.to_dict()

# --- create_humidity_gauge function (Adjusted for better visibility) ---
def create_humidity_gauge(df: pd.DataFrame) -> Dict[str, Any]:
    if df.empty or 'Humidity_percent' not in df.columns: return {}

    latest_humidity = df['Humidity_percent'].iloc[-1] 
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = latest_humidity,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': f"Humidity (%)", 'font': {'size': 20}}, # Title font size increased
        gauge = {
            'axis': {'range': [0, 100], 'tickwidth': 0, 'tickcolor': "rgba(255,255,255,0.7)"},
            'bar': {'color': "#3b82f6", 'thickness': 0.7}, # Bar thickness increased
            'bgcolor': "rgba(255,255,255,0.05)", 
            'steps' : [{'range': [0, 30], 'color': "#f87171"}, {'range': [30, 70], 'color': "#a7f3d0"}, {'range': [70, 100], 'color': "#3b82f6"}],
        },
        number={'font': {'color': '#3b82f6', 'size': 50}} # Number font size increased
    ))
    # Height adjusted to match new font sizes
    fig.update_layout(height=280, title_x=0.5, template="plotly_dark", margin=dict(l=20, r=20, t=60, b=10)) 
    return fig.to_dict()

# --- create_wind_gauge function (Adjusted for better visibility) ---
def create_wind_gauge(df: pd.DataFrame) -> Dict[str, Any]:
    if df.empty or 'Wind_Speed_m/s' not in df.columns: return {}

    latest_wind = df['Wind_Speed_m/s'].iloc[-1]
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = latest_wind,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': f"Wind Speed (m/s)", 'font': {'size': 20}}, # Title font size increased
        gauge = {
            'axis': {'range': [0, 20], 'tickwidth': 0, 'tickcolor': "rgba(255,255,255,0.7)"},
            'bar': {'color': "#fbbf24", 'thickness': 0.7}, # Bar thickness increased
            'bgcolor': "rgba(255,255,255,0.05)",
            'steps' : [{'range': [0, 5], 'color': "#a7f3d0"}, {'range': [5, 12], 'color': "#fbbf24"}, {'range': [12, 20], 'color': "#f87171"}],
        },
        number={'font': {'color': '#fbbf24', 'size': 50}} # Number font size increased
    ))
    # Height adjusted to match new font sizes
    fig.update_layout(height=280, title_x=0.5, template="plotly_dark", margin=dict(l=20, r=20, t=60, b=10))
    return fig.to_dict()

# --- create_summary_table function (No change) ---
def create_summary_table(df: pd.DataFrame):
    if df.empty: return html.Div("Data Summary N/A", className="text-muted p-3")
    latest = df.iloc[-1]
    
    visibility_m = latest.get('Visibility_m', 0)
    visibility_km = round(visibility_m / 1000, 1)

    data = [
        ("Description", latest['Weather_Description']),
        ("Feels Like", f"{latest['Feels_Like_C']:.1f} °C"), 
        ("Min Temp", f"{latest['Temp_Min_C']:.1f} °C"),
        ("Max Temp", f"{latest['Temp_Max_C']:.1f} °C"),
        ("Pressure", f"{latest['Pressure_hPa']} hPa"),
        ("Sea Level P.", f"{latest['Sea_Level_hPa']} hPa"),
        ("Ground Level P.", f"{latest['Grnd_Level_hPa']} hPa"),
        ("Wind Direction", f"{latest['Wind_Direction_deg']} degrees"),
        ("Cloud Cover", f"{latest['Clouds_percent']}%"),
        ("Visibility", f"{visibility_km} km"), 
    ]
    
    table_header = [html.Thead(html.Tr([html.Th("Metric"), html.Th("Value")]))]
    
    table_body = [html.Tbody([
        html.Tr([html.Td(row[0]), html.Td(row[1])]) for row in data
    ])]
    
    return dbc.Table(
        table_header + table_body,
        bordered=True,
        className="mt-2 table-dark table-sm"
    )