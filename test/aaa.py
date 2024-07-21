import streamlit as st
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo
import time
import wikipediaapi
from bs4 import BeautifulSoup
import requests

# Function to get the current time in a specific timezone
def get_time_in_timezone(timezone):
    tz = ZoneInfo(timezone)
    return datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')

# Function to get the current times for various regions
def get_current_times():
    timezones = {
        "한국": "Asia/Seoul",
        "미국(뉴욕)": "America/New_York",
        "일본": "Asia/Tokyo",
        "중국(베이징)": "Asia/Shanghai"
    }
    
    data = {
        '국가': [],
        '시간': [],
    }
    
    for region, tz in timezones.items():
        current_time = get_time_in_timezone(tz)
        data['국가'].append(region)
        data['시간'].append(current_time)

    return pd.DataFrame(data)

# Function to get the population of a country from Wikipedia
def get_population(country):
    wiki_wiki = wikipediaapi.Wikipedia('en')
    page = wiki_wiki.page(country)
    
    if page.exists():
        try:
            response = requests.get(page.fullurl)
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table', {'class': 'infobox'})
            for row in table.find_all('tr'):
                if 'Population' in row.text:
                    population = row.find('td').text.split('[')[0]
                    return population.strip()
        except Exception as e:
            st.error(f"Error fetching population for {country}: {e}")
            return None
    else:
        st.error(f"Wikipedia page does not exist for {country}")
        return None

# List of countries
countries = ["South Korea", "United States", "Japan", "China"]

# Get the population data for the countries
population_data = {country: get_population(country) for country in countries}

# Create a DataFrame for population data
population_df = pd.DataFrame([
    {'국가': country, '인구': pop} 
    for country, pop in population_data.items() if pop is not None
])

st.title("국가별 현재 시간 및 인구 데이터")

# Display current times
placeholder = st.empty()

# Display population data
st.subheader("국가별 인구 데이터")
st.write(population_df)

# Update the current times every second
while True:
    current_times_df = get_current_times()
    placeholder.write(current_times_df)
    time.sleep(1)

