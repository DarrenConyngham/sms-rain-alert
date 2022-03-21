import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient
import config  # config file contains api key, auth token, and phone numbers

OWM_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"

weather_params = {
    'lat': '-33.918861',
    'lon': '18.423300',
    'exclude':'current,minutely,daily',
    'units': 'metric',
    'appid': config.OWM_api_key
}


response = requests.get(OWM_Endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()
weather_slice = weather_data["hourly"][:12]

will_rain = False

for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    client = Client(config.twilio_account_sid, config.twilio_auth_token)
    message = client.messages \
        .create(
        body="It's going to rain today. Remember to bring an ☔️",
        from_=config.twilio_phone_num,
        to=config.my_phone_num
    )
    
    print(message.status)
