"""OpenWeatherMap API client."""

from __future__ import annotations

import os
from typing import Dict

import requests
from dotenv import load_dotenv

from .exceptions import CityNotFoundError, APICallFailedError
from .caching import load_cached_data, save_data_to_cache

load_dotenv()

BASE_URL = "http://api.openweathermap.org/data/2.5/weather"


def fetch_weather_data(city: str) -> Dict:
    """Fetch current weather data for a city using OpenWeatherMap's API."""
    if not city:
        raise ValueError("city must be provided")

    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    if not api_key:
        raise APICallFailedError("OPENWEATHERMAP_API_KEY is not configured.")

    cached = load_cached_data(city)
    if cached is not None:
        cached["_source"] = "cache"
        return cached

    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        data = response.json()
    except requests.RequestException as exc:
        raise APICallFailedError(f"API request failed: {exc}") from exc

    if response.status_code == 404 or str(data.get("cod")) == "404":
        raise CityNotFoundError(f"City '{city}' not found by OpenWeatherMap.")

    if not response.ok:
        raise APICallFailedError(
            f"HTTP {response.status_code}: {data.get('message', 'Unknown error')}"
        )

    save_data_to_cache(city, data)
    data["_source"] = "api"
    return data