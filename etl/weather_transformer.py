# etl/weather_transformer.py (ULTIMATE FINAL CODE)

import pandas as pd
from typing import Dict, Any

def transform_weather_data(raw_data: Dict[str, Any]) -> pd.DataFrame:
    """
    Raw OpenWeatherMap JSON data ko Pandas DataFrame mein transform karta hai, 
    jis mein saare available key features shamil hain.
    """
    
    if not isinstance(raw_data, dict) or 'main' not in raw_data:
        raise ValueError("Invalid or incomplete weather data received for transformation.")

    try:
        main_data = raw_data.get('main', {})
        weather_list = raw_data.get('weather', [{}])[0]
        wind_data = raw_data.get('wind', {})
        
        timestamp = raw_data.get('dt')
        city_name = raw_data.get('name', 'N/A')
        
        # --- Saare Key Features Shamil Kiye Gaye Hain ---
        transformed_record = {
            'City': city_name,
            'Timestamp': pd.to_datetime(timestamp, unit='s'),
            
            # Temperature and Feeling Metrics (Sabse zaroori)
            'Temperature_C': main_data.get('temp'),
            'Feels_Like_C': main_data.get('feels_like'), # NEW
            'Temp_Min_C': main_data.get('temp_min'),       # NEW
            'Temp_Max_C': main_data.get('temp_max'),       # NEW
            
            # Pressure Metrics (NEW)
            'Pressure_hPa': main_data.get('pressure'),
            'Sea_Level_hPa': main_data.get('sea_level'), # NEW
            'Grnd_Level_hPa': main_data.get('grnd_level'), # NEW
            
            # Other Key Metrics
            'Humidity_percent': main_data.get('humidity'),
            'Wind_Speed_m/s': wind_data.get('speed'),
            'Wind_Direction_deg': wind_data.get('deg'),
            'Weather_Description': weather_list.get('description', 'N/A').title(),
            'Clouds_percent': raw_data.get('clouds', {}).get('all', 0),
            'Visibility_m': raw_data.get('visibility')
        }
        
    except Exception as e:
        raise TypeError(f"Error during weather data transformation: {e}")

    df = pd.DataFrame([transformed_record])
    df = df.set_index('Timestamp')
    
    # Data Types ko confirm karna (zyada tar data floats honge)
    df['Temperature_C'] = df['Temperature_C'].astype(float)
    df['Humidity_percent'] = df['Humidity_percent'].astype('Int64') # Int64 for potential NaN handling
    
    return df