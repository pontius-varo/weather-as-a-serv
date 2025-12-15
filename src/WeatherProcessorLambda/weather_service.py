import os
import requests


def c_to_f(c: float) -> float:
    return (c * 9.0 / 5.0) + 32.0


def get_weather(location: str) -> dict:
    provider = os.environ.get("WEATHER_PROVIDER", "openweather").lower()
    if provider != "openweather":
        raise ValueError(f"Unsupported WEATHER_PROVIDER: {provider}")

    api_key = os.environ.get("WEATHER_API_KEY", "").strip()
    if not api_key:
        raise ValueError("WEATHER_API_KEY is required.")

    # OpenWeather "Current Weather Data" endpoint
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": location,
        "appid": api_key,
        "units": "metric",  # returns temp in Celsius
    }

    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    temp_c = float(data["main"]["temp"])
    temp_f = float(c_to_f(temp_c))
    conditions = (data.get("weather") or [{}])[0].get("description", "unknown").title()

    # Use canonical city name if returned
    resolved_name = data.get("name") or location
    country = (data.get("sys") or {}).get("country")
    resolved_location = f"{resolved_name}, {country}" if country else resolved_name

    return {
        "location": resolved_location,
        "temp_c": round(temp_c, 1),
        "temp_f": round(temp_f, 1),
        "conditions": conditions,
    }
