import streamlit as st
import requests
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(page_title="Weather Dashboard", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp {
        background-color: black;
    }
    .main {
        padding: 20px;
    }
    .stMetric {
        background-color: #f0f2f5;
        padding: 10px;
        border-radius: 10px;
    }
    div[data-testid="stToolbar"] {
        display: none;
    }
    #MainMenu {
        visibility: hidden;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Weather Dashboard")

# API settings
API_KEY = os.getenv('OPENWEATHER_API_KEY')
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# City input
city = st.text_input("Enter City Name", placeholder="e.g., New York")

if city:
    # Show loading spinner
    with st.spinner('Fetching weather data...'):
        # API call
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'imperial'
        }
        
        try:
            response = requests.get(BASE_URL, params=params)
            data = response.json()
            
            if response.status_code == 200:
                # Create columns for layout
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Temperature", f"{round(data['main']['temp'])}°F")
                    st.metric("Humidity", f"{data['main']['humidity']}%")
                
                with col2:
                    st.metric("Wind Speed", f"{round(data['wind']['speed'])} mph")
                    st.write(f"Description: {data['weather'][0]['description'].capitalize()}")
                    
                st.caption(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")
            else:
                st.error("City not found. Please check the city name and try again.")
                
        except Exception as e:
            st.error("Error fetching weather data. Please try again later.")