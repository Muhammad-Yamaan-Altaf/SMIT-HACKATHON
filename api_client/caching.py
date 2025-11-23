# api_client/caching.py

import json
import os
import time
from typing import Optional, Dict, Any

# Caching ki settings
CACHE_DIR = "cache"
# Data ki hadd (maximum age): 10 minutes (600 seconds)
MAX_CACHE_AGE = 600 

def get_cache_filepath(city: str) -> str:
    """ City name se cache file ka path return karta hai. """
    # File name mein spaces (jagah) ki bajaye underscore ka istemaal karein
    filename = f"{city.lower().replace(' ', '_')}.json"
    return os.path.join(CACHE_DIR, filename)

def load_cached_data(city: str) -> Optional[Dict[str, Any]]:
    """
    Cache se data load karta hai agar woh fresh (taza) ho.
    """
    filepath = get_cache_filepath(city)
    
    # 1. Check karein ke file maujood hai ya nahin
    if not os.path.exists(filepath):
        return None
        
    # 2. File ki age check karein
    file_age = time.time() - os.path.getmtime(filepath)
    
    if file_age > MAX_CACHE_AGE:
        # Data purana (stale) ho gaya hai
        print(f"Cache for {city} is stale ({file_age:.0f}s old). Deleting.")
        os.remove(filepath)
        return None
        
    # 3. Data load karein
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            print(f"Loading data for {city} from cache.")
            return json.load(f)
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error reading cache file for {city}: {e}")
        return None

def save_data_to_cache(city: str, data: Dict[str, Any]):
    """
    Data ko local JSON file mein save karta hai.
    """
    filepath = get_cache_filepath(city)
    
    # Cache directory banaein agar woh maujood na ho
    os.makedirs(CACHE_DIR, exist_ok=True)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        # print(f"Data saved to cache for {city}.")
    except IOError as e:
        print(f"Error saving data to cache for {city}: {e}")