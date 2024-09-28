from django.shortcuts import render
import requests, json, os
from django.http import JsonResponse
from django.conf import settings

# Home page view
def home(request):
    return render(request, 'weather/home.html')

# Map view to render the map page
def map_view(request):
    return render(request, 'weather/bymap.html')

# Fetch weather data using latitude and longitude
def get_weather(request):
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')


    api_key = 'your_api_key_here'
    
    # URL to OpenWeatherMap API
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric'

    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            # Extract weather information if API call is successful
            weather = {
                'description': data['weather'][0]['description'],
                'temperature': data['main']['temp'],
            }
        else:
            weather = {'error': 'Unable to fetch weather data'}
    except requests.exceptions.RequestException as e:
        # Handle request exceptions
        weather = {'error': str(e)}

    return JsonResponse(weather)

# Function to load locations from a JSON file
def load_locations():
    data_path = os.path.join(settings.BASE_DIR, 'weather', 'data', 'locations.json')
    with open(data_path, encoding='utf-8') as f:
        return json.load(f)

# Weather view based on city input
def index(request):
    locations = load_locations()  # Load locations for dropdown
    selected_country = request.GET.get('country', '')
    selected_state = request.GET.get('state', '')
    selected_city = request.GET.get('city', '')
    selected_city_name = request.GET.get('city_name', '')

    # Prioritize selected_city, fallback to city_name
    city = selected_city if selected_city else selected_city_name

    data = None

    if city:
        api_key = 'your_api_key_here'
        # URL to OpenWeatherMap API for city-based weather data
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        try:
            response = requests.get(url)
            weather_data = response.json()

            if response.status_code == 200 and weather_data['cod'] == 200:
                # Store weather data if successful
                data = {
                    'city': city,
                    'temperature': weather_data['main']['temp'],
                    'description': weather_data['weather'][0]['description'],
                    'icon': weather_data['weather'][0]['icon'],
                    'humidity': weather_data['main']['humidity'],
                    'wind_speed': weather_data['wind']['speed'],
                    'error': None
                }
            else:
                data = {'error': 'City not found'}
        except requests.exceptions.RequestException as e:
            # Handle request exceptions
            data = {'error': str(e)}

    # Render bycity.html with weather data and location options
    return render(request, 'weather/bycity.html', {'data': data, 'locations': locations})
