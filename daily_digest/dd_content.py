import csv
import random
import os
import json
import datetime
from dotenv import load_dotenv
from urllib import request, parse


def get_random_quote(quotes_file):
    quotes = []
    with open(quotes_file, 'r', encoding='utf-8') as csvfile:
        for linea in csv.reader(csvfile, delimiter = "|"):
            quotes.append({"author": linea[0].strip(),
                           "quote": linea[1].strip()})
            
    return random.choice(quotes)

def get_weather_forecast():
    load_dotenv()
    api_key = os.getenv("apikey")
    # print("api key:", api_key) # la api key se carga bien

    # city_name = input("Enter city name:")
    city_name = 'parana'
    geourl = f'http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=3&appid={api_key}'
    geodata = json.load(request.urlopen(geourl))
    # print(data)

    lat = geodata[0]['lat']
    # print(lat)
    lon = geodata[0]['lon']
    # print(lon)

    forecasturl = f'http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=es'
    forecastdata = json.load(request.urlopen(forecasturl))

    # print(type(forecastdata)) # dict
    # print(forecastdata['list'][1]['main']['temp'])

    forecast = {'city': forecastdata['city']['name'],
                'country': forecastdata['city']['country'],
                'periods': list()}
    
    # print("forecastdata['list']:", type(forecastdata['list'])) # list
    # print(len(forecastdata['list'])) # 40
    for period in forecastdata['list'][0:9]:
        forecast['periods'].append({'timestamp': datetime.datetime.fromtimestamp(period['dt']),
                                    'temp': round(period['main']['temp']),
                                    'description': period['weather'][0]['description'].title(),
                                    'icon': f"http://openweathermap.org/img/wn/{period['weather'][0]['icon']}.png"})
      
    return forecast

# def get_wikipedia_article(limit=5):
#     wikiurl = 'https://en.wikipedia.org/w/api.php'
#     params = {
#         "action": "query",
#         "format": "json",
#         "list": "random",
#         "rnlimit": str(limit)
#     }
#     query = parse.urlencode(params)
#     req = request.Request(
#         f"{wikiurl}?{query}",
#         headers={"User-Agent": "daily-digest/1.0 (https://example.com)"}
#     )
#     wikidata = json.load(request.urlopen(req))
#     randoms = wikidata.get("query", {}).get("random", [])
#     return [item["title"] for item in randoms]

def get_wikipedia_article():
    try:
        url = 'https://en.wikipedia.org/api/rest_v1/page/random/summary'
        
        headers = {'User-Agent': 'YourDailyDigest/1.0 (your_email@example.com)'}
        req = request.Request(url, headers=headers)
        
        with request.urlopen(req) as response:
            data = json.load(response)
        
        return {
            'title': data['title'],
            'extract': data['extract'],
            'url': data['content_urls']['desktop']['page']
        }
        
    except Exception as e:
        print(f"Error fetching Wikipedia article: {e}")

if __name__ == "__main__":
    quote = get_random_quote("./daily_digest/frases.csv")
    print(f'{quote["author"]} | {quote["quote"]}')

    forecast = get_weather_forecast()
    print(f'\nWeather forecast for {forecast["city"]}, {forecast["country"]} is...')
    for period in forecast['periods']:
        print(f' - {period["timestamp"]} | {period["temp"]}°C | {period["description"]}')

    article = get_wikipedia_article()
    if article:
        print(f'\n{article["title"]}\n<{article["url"]}>\n{article["extract"]}')