# dashboard/app.py (FINAL COMPLETE VERSION - Reading README.md)

import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc 
import plotly.graph_objects as go
import os # Naya import: File operations ke liye

# Import karein apne modules:
from api_client.openweathermap import fetch_weather_data
from api_client.exceptions import CityNotFoundError, APICallFailedError
from etl.weather_transformer import transform_weather_data
from analysis.visualizations import (
    create_temperature_chart, 
    create_humidity_gauge, 
    create_wind_gauge, 
    create_summary_table 
)

# --- README FILE READING LOGIC ---
def load_readme_content():
    """Reads the content of the README.md file from the root directory."""
    # Note: Hum jante hain ke 'main.py' se chalane par root directory 'ETL_Project' hoti hai
    readme_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'README.md')
    try:
        # File ko 'utf-8' encoding ke saath read karein
        with open(readme_path, 'r', encoding='utf-8') as f:
            # Markdown file mein se sirf description ka hissa nikal sakte hain (optional)
            content = f.read()
            # Hum poora content display kar rahe hain
            return content
    except FileNotFoundError:
        return "### ERROR: README.md file not found in the project root directory. Please create it."

PROJECT_DESCRIPTION = load_readme_content()
# --- End of README File Reading Logic ---

EXTERNAL_STYLESHEETS = [dbc.themes.DARKLY] 
app = dash.Dash(__name__, external_stylesheets=EXTERNAL_STYLESHEETS)

DEFAULT_CITY = "Karachi" 

def create_empty_figure(title):
    fig = go.Figure()
    fig.update_layout(
        template="plotly_dark", 
        xaxis={'visible': False},
        yaxis={'visible': False},
        height=280, 
        annotations=[
            {'text': title, 
             'xref': "paper", 
             'yref': "paper", 
             'showarrow': False, 
             'font': {'size': 20, 'color': '#AAAAAA'}}
        ]
    )
    return fig.to_dict()

# 2. Application Layout Define Karein
app.layout = dbc.Container([
    # Header 
    dbc.Row(dbc.Col(
        html.H1("Advanced Weather ETL Dashboard", 
                className="text-center text-info mb-4", 
                style={'paddingTop': '20px', 'letterSpacing': '2px'}
        )
    )),
    
    # Input Card and Visuals Rows... (Remaining layout code is the same)
    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col(dbc.Input(
                    id='city-input',
                    value=DEFAULT_CITY,
                    type='text',
                    placeholder='Enter City (e.g., London, Tokyo)',
                ), md=9),
                dbc.Col(dbc.Button(
                    'FETCH & ANALYZE', 
                    id='submit-button', 
                    n_clicks=0, 
                    color="info", 
                    className="w-100"
                ), md=3)
            ], className="g-2"),
            
            dbc.Row(dbc.Col(
                html.Div(id='output-message', 
                         className="text-center mt-3 font-weight-bold"
                )
            ))
        ]),
        className="mb-4 shadow-lg border-info" 
    ),

    # Main Visuals Row
    dbc.Row([
        dbc.Col(
            dbc.Card(
                dcc.Graph(
                    id='temperature-graph',
                    figure=create_empty_figure("Temperature Data"),
                    config={'displayModeBar': False}
                ),
                className="shadow-sm border-light h-100"
            ), 
            md=9 
        ),
        
        dbc.Col(
            dbc.Card(
                dbc.CardBody(id='summary-table-output', className="h-100 p-2"), 
                className="shadow-sm border-light h-100"
            ), 
            md=3
        )
    ], className="mb-4"),
    
    # Gauge Charts Row
    dbc.Row([
        dbc.Col(
            dbc.Card(
                dcc.Graph(id='humidity-gauge', 
                          figure=create_empty_figure("Humidity Gauge"),
                          config={'displayModeBar': False}),
                className="shadow-sm border-light"
            ), 
            md=6
        ),
        
        dbc.Col(
            dbc.Card(
                dcc.Graph(id='wind-gauge', 
                          figure=create_empty_figure("Wind Speed Gauge"),
                          config={'displayModeBar': False}),
                className="shadow-sm border-light"
            ), 
            md=6
        )
    ], className="mb-4"),
    
    # --- Project Documentation / README Section ---
    dbc.Row(dbc.Col(
        dbc.Card(dbc.CardBody([
            # Ab yeh variable file ka content utha raha hai
            dcc.Markdown(PROJECT_DESCRIPTION, className="text-light"), 
            html.Hr(className="bg-info"), 
            html.P("Technology Stack: Python, Dash, Plotly, Dash Bootstrap Components.", className="text-muted small")
        ])),
        className="mt-4 mb-4 shadow-lg border-info" 
    )),
    # --- End of Documentation Section ---

    dbc.Row(dbc.Col(
        html.Footer("Weather ETL System | Professional Build", className="text-center text-muted mt-5 mb-3")
    ))
], fluid=True, style={'maxWidth': '1400px'})

# 3. Callbacks Define Karein (No change)
@app.callback(
    [Output('output-message', 'children'),
     Output('temperature-graph', 'figure'),
     Output('humidity-gauge', 'figure'),
     Output('wind-gauge', 'figure'), 
     Output('summary-table-output', 'children')], 
    [Input('submit-button', 'n_clicks')],
    [State('city-input', 'value')]
)
def update_dashboard(n_clicks, city_name):
    # ... (Callback logic remains the same)
    
    empty_temp = create_empty_figure("Temperature Data")
    empty_humid = create_empty_figure("Humidity Gauge")
    empty_wind = create_empty_figure("Wind Speed Gauge")
    empty_table = html.Div("Data Summary N/A", className="text-muted p-3")
    
    if not city_name:
        return (dbc.Alert("⚠️ Please enter a City Name.", color="warning"), 
                empty_temp, empty_humid, empty_wind, empty_table)

    try:
        raw_data = fetch_weather_data(city=city_name) 
        cleaned_df = transform_weather_data(raw_data)
        
        temp_fig = create_temperature_chart(cleaned_df)
        humid_fig = create_humidity_gauge(cleaned_df)
        wind_fig = create_wind_gauge(cleaned_df)
        summary_table = create_summary_table(cleaned_df)
        
        source = 'Cache' if raw_data.get('cached') else 'API'
        return (dbc.Alert(f"✅ Data fetched for {city_name} (Source: {source}).", color="success"), 
                temp_fig, humid_fig, wind_fig, summary_table)

    except CityNotFoundError:
        return (dbc.Alert(f"❌ Error: City '{city_name}' not found.", color="danger"), 
                empty_temp, empty_humid, empty_wind, empty_table)
    except APICallFailedError as e:
        return (dbc.Alert(f"❌ API Failure: {e}", color="danger"), 
                empty_temp, empty_humid, empty_wind, empty_table)
    except Exception as e:
        return (dbc.Alert(f"❌ An unexpected error occurred: {e}", color="danger"), 
                empty_temp, empty_humid, empty_wind, empty_table)