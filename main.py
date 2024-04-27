import requests
from bs4 import BeautifulSoup
from to_exel import ExcelManager
from random import randint

manager = ExcelManager('test_1.xlsx', ['title', 'location', 'city', 'room', 'beth', 'area', 'price'])

SCRAPEOPS_API_KEY = 'e8ebf62a-16df-4639-ad3a-05a83089fc89'


def get_user_agent_list():
    response = requests.get('http://headers.scrapeops.io/v1/user-agents?api_key=' + SCRAPEOPS_API_KEY)
    json_response = response.json()
    return json_response.get('result', [])


def get_random_user_agent(user_agent_list):
    random_index = randint(0, len(user_agent_list) - 1)
    return user_agent_list[random_index]


def fetch_data(soup):
    prices = [price.text_content() for price in
              soup.select('ul[role=list] div[class^=styles-module_content__price-area]')]
    titles = [title.text_content() for title in
              soup.select('ul[role=list] h2[class^=styles-module_content__title]')]
    locations = [location.text_content() for location in
                 soup.select('ul[role=list] p[class^=styles-module_content__location]')]
    detail_rooms = soup.select('ul[role=list] p[class^=styles-module_content__details-item]')
    rooms = [room.text_content() for room in detail_rooms[0: len(detail_rooms): 3]]
    beths = [beth.text_content() for beth in
             detail_rooms[1: len(detail_rooms): 3]]
    areas = [area.text_content() for area in
             detail_rooms[2: len(detail_rooms): 3]]
    data = []
    for price, title, location, room, beth, area in zip(prices, titles, locations, rooms, beths, areas):
        city = location.split(', ')[-1]
        data.append([
            title.strip(),
            location.strip(),
            city,
            room.strip(),
            beth.strip(),
            area.strip(),
            price.strip(),
        ])
    return data


# 595

headers = {'User-Agent': get_random_user_agent(get_user_agent_list())}
clean_data = []
for _ in range(1, 50):
    url = f'https://www.propertyfinder.ae/en/search?l=50-71-36-86-67&c=1&fu=0&ob=mr&page={_}'
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    clean_data = fetch_data(soup)
    manager.save_to_excel(clean_data)
