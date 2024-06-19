import requests # Import the requests library
from stringcolor import cs

def get_ip_address():
    # Make a request to get the user's IP address
    response = requests.get('https://api.ipify.org?format=json')
    data = response.json()
    return data['ip']

def get_location_data(ip):
    # Make a request to get location data based on the user's IP address
    response = requests.get(f'http://ip-api.com/json/{ip}')
    data = response.json()
    return data['lat'], data['lon']

def get_weather_data(lat, lon, api_key):
    # Make a request to the OpenWeatherMap API to get weather data for the given coordinates
    url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric'
    response = requests.get(url)
    data = response.json()
    return data

def main():
    ip = get_ip_address() # Get the user's IP address
    lat, lon = get_location_data(ip) # Get the user's location data
    api_key = '3aa893356a2abcb99d114ef02e82e006' # Replace 'YOUR_API_KEY' with your OpenWeatherMap API key
    weather_data = get_weather_data(lat, lon, api_key) # Get the weather data

    # Display the weather data
    print(cs("Current Weather:", "yellow"))
    print(f"Temperature: {weather_data['main']['temp']}°C")
    print(f"Weather: {weather_data['weather'][0]['main']}")
    print(f"Humidity: {weather_data['main']['humidity']}%")
    if 'rain' in weather_data:
        rain_volume = weather_data['rain'].get('1h', 0)  # Get precipitation volume for the last 1 hour
        print(f"Precipitation (last 1 hour): {rain_volume} mm")
    else:
        print("Precipitation (last 1 hour): 0 mm")

if __name__ == "__main__":
    main()
