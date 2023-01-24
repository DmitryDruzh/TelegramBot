from bs4 import BeautifulSoup as bs
from datetime import datetime
import requests


url = 'https://www.nn.rhl.su/calendar/calendar/18--1-2022-2023'

event = {'opponent': None,
        'date': None,
        'place': None,
        'result': None}

response = requests.get(url)
if response.status_code == 200:
    soup = bs(response.text, 'html.parser')
    # teams_at_home = soup.findAll('div', class_="jstable-cell jsMatchDivHome jscal_notplayed")
    # teams_visitors = soup.findAll('div', class_="jstable-cell jsMatchDivAway jscal_notplayed")
    game_ikar = soup.findAll('div', string='Икар')
    for game in game_ikar:
        non_played = game.findParent('div', class_="jstable-cell jsMatchDivHome jscal_notplayed")
        if non_played is None:
            non_played = game.findParent('div', class_="jstable-cell jsMatchDivAway jscal_notplayed")
        if non_played is not None:
            event['place'] = non_played.find_next_sibling().text
            details = []
            for detail in non_played.find_previous_siblings():
                if detail.text.strip():
                    details.append(detail.text.strip())
            print(details)
            event['result'] = details[0]
            event['opponent'] = details[1]
            event['date'] = datetime.strptime(details[2], '%d-%m-%Y %H:%M')


