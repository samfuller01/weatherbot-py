import requests, os, discord, logging
from dotenv import load_dotenv
load_dotenv()

# print(data['weather'][0]['main'])

logging.basicConfig(level=logging.INFO)


class WeatherBot(discord.Client):
    async def on_ready(self):
        print('Logged in as {0}!'.format(self.user))

    def get_weather(self, query, units):
        weather_api_key = os.getenv('API_KEY')
        r = requests.get('https://api.openweathermap.org/data/2.5/weather?q={0}&appid={1}&units={2}'.format(query, weather_api_key, units))
        return r.json()

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('!weather'):
            # try:
            args = message.content.split(' ')
            unit = args[2] if len(args) > 2 else 'imperial'
            data = self.get_weather(args[1], unit)
            await message.channel.send('Current weather in {0} is `{1}` with a temperature of {2} degrees. It feels like {3} degrees though.'.format(args[1], data['weather'][0]['main'], data['main']['temp'], data['main']['feels_like']))
        # except:
                # await message.channel.send('Getting weather data failed.')

client = WeatherBot()
client.run(os.getenv('TOKEN'))
