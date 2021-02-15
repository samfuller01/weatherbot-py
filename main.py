import requests, os, discord, sys
from discord.ext import commands
from geopy.geocoders import Nominatim
from functools import partial
from dotenv import load_dotenv
load_dotenv()


# Logging if in dev mode
if len(sys.argv) > 1 and sys.argv[1] == 'dev':
    import logging
    logging.basicConfig(level=logging.INFO)

class WeatherBot(commands.Bot):
    async def on_ready(self):
        await self.change_presence(status=discord.Status.online, activity=discord.Game('cloud watching'))
        print('Logged in as {0}!'.format(self.user))

def geocoder(location):
    geolocator = Nominatim(user_agent='WeatherBot - Discord bot for checking weather around the world.')
    geocode = partial(geolocator.geocode, language='en')
    return geocode(location)

def get_weather(location, units):
    weather_api_key = os.getenv('API_KEY')
    location_lat = geocoder(location).latitude
    location_lon = geocoder(location).longitude
    api_url = f'https://api.openweathermap.org/data/2.5/onecall?lat={location_lat}&lon={location_lon}&exclude=minutely,hourly,alerts&appid={weather_api_key}&units={units}'
    r = requests.get(api_url)
    return r.json()

wb = WeatherBot(command_prefix=os.getenv('PREFIX'))

@wb.command()
async def cweather(ctx, location, units='imperial'): 
    data = get_weather(location, units)
    await ctx.send(
        'Current weather is `{0}` with a temp of {1}. It feels like {2}.'
        .format(data['current']['weather'][0]['description'], data['current']['temp'], data['current']['feels_like'])
    )

@wb.command()
async def dweather(ctx, location, units='imperial'):
    await ctx.send('Daily weather feature coming soon!')

@wb.command()
async def help(ctx):
    await ctx.send('Help message coming soon. for now just use $cweather. locations can be addresses (wraped in quotation marks!!!), cities, or zip codes.')

wb.run(os.getenv('TOKEN'))
