#!/usr/bin/env python
# coding: utf-8

# In[4]:


import requests
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter


# In[81]:


cities = [
    ["Tehran", "Iran"], 
    ["Ottawa", "Canada"], 
    ["Seoul", "South Korea"], 
    ["Madrid", "Spain"], 
    ["Tokyo", "Japan"],
    ["Kyiv", "Ukraine"],
    ["Warsaw", "Poland"],
    ["Berlin", "Germany"],
    ["London", "UK"],
    ["Madrid", "Spain"],
    ["Paris", "France"],
    ["Rome", "Italy"],
    ["Prague", "Czechia"],
    ["Istanbul", "Turkey"],
    ["Stockholm", "Sweden"],
    ["Sofia", "Bulgaria"],
    ["Bucharest", "Romania"],
    ["Zurich", "Switzerland"],
]
df = pd.DataFrame(cities, columns=["city", "country"])


# In[88]:


locator = Nominatim(user_agent="myGeocoder")
geocode = RateLimiter(locator.geocode, min_delay_seconds=.1)

def get_coordinates(city, country):
  response = geocode(query={"city": city, "country": country})
  return {
    "latitude": response.latitude,
    "longitude": response.longitude
  }

df_coordinates = df.apply (lambda x: get_coordinates(x.city, x.country), axis=1)
df = pd.concat([df, pd.json_normalize(df_coordinates)], axis=1)


# In[91]:


import datetime

def get_weather(row):

  url = "https://api.openweathermap.org/data/2.5/weather?lat={row.latitude}&lon={row.longitude}&appid={59f4f19939715e5bd6e8286531137188}"
  my_response = requests.get(url)
  data = my_response.json()

  return {
      "temp": data["main"]["temp"] - 273.15,
      "pressure": data["weather"][0]["pressure"],
      "humidity":data["weather"][0]["humidity"],
      "description": data["weather"][0]["description"],
      "icon": data["weather"][0]["icon"],
  }

df_weather = df.apply (lambda x: get_weather(x), axis=1)
df = pd.concat ([df, pd.json_normalize(df_weather)], axis=1)



# In[94]:


def get_air_pollution(row):

  url = "http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API key}?lat={row.latitude}&lon={row.longitude}&appid={59f4f19939715e5bd6e8286531137188}"
  my_response = requests.get(url)
  data = my_response.json()

  return {
      "temp": data["main"]["aqi"]
  }

df_air_pollution = df.apply (lambda x: get_air_pollution(x), axis=1)
df = pd.concat ([df, pd.json_normalize(df_air_pollution)], axis=1)


# In[ ]:




