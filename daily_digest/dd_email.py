from dd_content import get_random_quote, get_weather_forecast, get_wikipedia_article
import datetime

class DailyDigestEmail:
    def __init__(self):
        self.content = {'quote': {'include': True, 'content': get_random_quote("./daily_digest/frases.csv")},
                        'weather': {'include': True, 'content': get_weather_forecast()},
                        'article': {'include': True, 'content': get_wikipedia_article()}}

    def format_message(self):
        text = f'*~*~*~*~* Daily Digest - {datetime.date.today().strftime("%d %b %Y")} *~*~*~*~*\n\n'

        # plain text format

        # format random quote
        if self.content['quote']['include'] and self.content['quote']['content']:
            text += '*~*~* Quote of the Day *~*~*\n\n'
            text += f'"{self.content["quote"]["content"]["quote"]}" - {self.content["quote"]["content"]["author"]}\n\n'

        # format weather forecast
        if self.content['weather']['include'] and self.content['weather']['content']:
            text += f'*~*~* Forecast for {self.content["weather"]["content"]["city"]}, {self.content["weather"]["content"]["country"]} *~*~*\n\n'
            for forecast in self.content['weather']['content']['periods']:
                text += f'{forecast["timestamp"].strftime("%d %b %H%M")} - {forecast["temp"]}\u00B0C | {forecast["description"]}\n'
            text += '\n'

        # format wikipedia article
        if self.content['article']['include'] and self.content['article']['content']:
            text += '*~*~* Daily Random Learning *~*~*\n\n'
            text += f'{self.content["article"]["content"]["title"]}\n{self.content["article"]["content"]["extract"]}'

        return text

    def send_email(self):
        pass



if __name__ == "__main__":
    email = DailyDigestEmail()

    # test format_message() 
    message = email.format_message()

    with open('./daily_digest/message_text.txt', 'w', encoding='utf-8') as f:
        f.write(message)