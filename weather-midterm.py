import requests
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from prettytable import PrettyTable


# City list
cities = [
    "Tehran, Iran",
    "Ottawa, Canada",
    "Seoul, South Korea",
    "Madrid, Spain",
    "Tokyo, Japan",
    "Kyiv, Ukraine",
    "Warsaw, Poland",
    "Berlin, Germany",
    "London, UK",
    "Madrid, Spain",
    "Paris, France",
    "Rome, Italy",
    "Prague, Czechia",
    "Istanbul, Turkey",
    "Stockholm, Sweden",
    "Sofia, Bulgaria",
    "Bucharest, Romania",
    "Zurich, Switzerland",
]

# Create dataframe
df = pd.DataFrame(cities, columns=["city"])

# Function for coordinates
def get_coordinates(city):
    locator = Nominatim(user_agent="myGeocoder")
    location = locator.geocode(city)
    if location:
        return {
            "latitude": location.latitude,
            "longitude": location.longitude
        }
    else:
        return {
            "latitude": None,
            "longitude": None
        }

# Function for weathers data
def get_weather(latitude, longitude):
    api_key = "YOUR_API_KEY"  # Enter your Api key
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    if "main" in data and "weather" in data:
        return {
            "temp": data["main"]["temp"] - 273.15,
            "pressure": data["main"]["pressure"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"],
            "icon": data["weather"][0]["icon"],
        }
    else:
        return {
            "temp": None,
            "pressure": None,
            "humidity": None,
            "description": None,
            "icon": None,
        }

# Function for Air Polution
def get_air_pollution(latitude, longitude):
    api_key = "YOUR_API_KEY"  #Enter your Api key
    url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={latitude}&lon={longitude}&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    if "list" in data and len(data["list"]) > 0 and "main" in data["list"][0]:
        return {
            "aqi": data["list"][0]["main"]["aqi"]
        }
    else:
        return {
            "aqi": None
        }


# Create new culomns for weather data
df["coordinates"] = df["city"].apply(get_coordinates)
df["latitude"] = df["coordinates"].apply(lambda x: x["latitude"])
df["longitude"] = df["coordinates"].apply(lambda x: x["longitude"])
df["weather"] = df.apply(lambda row: get_weather(row["latitude"], row["longitude"]), axis=1)
df["air_quality"] = df.apply(lambda row: get_air_pollution(row["latitude"], row["longitude"]), axis=1)

print (df)
