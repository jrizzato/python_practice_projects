from dd_content import get_random_quote, get_weather_forecast, get_wikipedia_article
from dotenv import load_dotenv
from email.message import EmailMessage
import datetime
import os
import smtplib

class DailyDigestEmail:
    def __init__(self):
        self.content = {'quote': {'include': True, 'content': get_random_quote("./daily_digest/frases.csv")},
                        'weather': {'include': True, 'content': get_weather_forecast()},
                        'article': {'include': True, 'content': get_wikipedia_article()}}
        load_dotenv()
        digest_recipient1 = os.getenv("digest_recipient1")
        sender_email = os.getenv("email")
        sender_password = os.getenv("password")

        self.recipient_list = [digest_recipient1]

        self.sender_credentials = {'email': sender_email,
                                   'password': sender_password}

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
                text += f'{forecast["timestamp"].strftime("%d %b %H:%M")} - {forecast["temp"]}\u00B0C | {forecast["description"]}\n'
            text += '\n'

        # format wikipedia article
        if self.content['article']['include'] and self.content['article']['content']:
            text += '*~*~* Daily Random Learning *~*~*\n\n'
            text += f'{self.content["article"]["content"]["title"]}\n{self.content["article"]["content"]["extract"]}'

        return text

    def send_email(self):
        # build email message

        msg = EmailMessage()
        msg['Subject'] = f'Daily Digest - {datetime.date.today().strftime("%d %b %Y")}'
        msg['From'] = self.sender_credentials['email']
        msg['To'] = ', '.join(self.recipient_list)

        msg_body = self.format_message()
        msg.set_content(msg_body)

        # secure connection with SMTP server and send email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(self.sender_credentials['email'],
                         self.sender_credentials['password'])
            server.send_message(msg)



if __name__ == "__main__":
    email = DailyDigestEmail()

    # test format_message() 
    message = email.format_message()

    with open('./daily_digest/message_text.txt', 'w', encoding='utf-8') as f:
        f.write(message)

    email.send_email()