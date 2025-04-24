import streamlit as st
import requests
import plotly.express as px

# API key from file:
api_key = st.secrets["openweather"]["api_key"]

# Set Cache-s:
@st.cache_data
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
        
# Plotly map:
def show_map(lat, lon, city_name):
    fig = px.scatter_mapbox(
        lat=[lat],
        lon=[lon],
        text=[city_name],
        zoom=10,
        height=500
    )
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_traces(marker=dict(size=14, color="red"))
    return fig

# User Interface:
st.title("Real-time Weather App")

city = st.text_input("Enter city name", "London")

if city:
    weather = get_weather(city)

    if weather:
        st.subheader(f"Current Weather in {city}")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Temperature (°C)", f"{weather['main']['temp']} °C")
        with col2:
            st.metric("Humidity (%)", f"{weather['main']['humidity']} %")
        with col3:
            st.metric("Wind Speed (m/s)", f"{weather['wind']['speed']} m/s")

        st.subheader("City on Map")
        lat = weather["coord"]["lat"]
        lon = weather["coord"]["lon"]
        fig = show_map(lat, lon, city)
        st.plotly_chart(fig)

    else:
        st.error("City not found or error fetching data.")