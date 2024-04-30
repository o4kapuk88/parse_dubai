from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from to_exel import ExcelManager

manager = ExcelManager('test.xlsx', ['title', 'location', 'city', 'room', 'beth', 'area', 'price'])


def fetch_data(page):
    prices = [price.text_content() for price in
              page.query_selector_all('ul[role=list] div[class^=styles-module_content__price-area]')]
    titles = [title.text_content() for title in
              page.query_selector_all('ul[role=list] h2[class^=styles-module_content__title]')]
    locations = [location.text_content() for location in
                 page.query_selector_all('ul[role=list] p[class^=styles-module_content__location]')]

    rooms = [_.inner_text() for _ in page.query_selector_all('ul[role=list] p[data-testid=property-card-spec-bedroom]')]
    beths = [_.inner_text() for _ in page.query_selector_all('ul[role=list] p[data-testid=property-card-spec-bathroom]')]
    areas = [_.inner_text() for _ in page.query_selector_all('ul[role=list] p[data-testid=property-card-spec-area]')]
    data = []
    for price, title, location, room, beth, area in zip(prices, titles, locations, rooms, beths, areas):
        city = location.split(', ')[-1]
        data.append([
            title.strip(),
            location.strip(),
            city.strip(),
            room.strip(),
            beth.strip(),
            area.strip(),
            price.strip(),
        ])
    return data


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')
    page = context.new_page()

    for i in range(1, 578):
        url = f'https://www.propertyfinder.ae/en/search?l=50-71-36-86-67-89&c=1&fu=0&ob=mr&page={i}'
        page.goto(url, timeout=900000)
        soup = BeautifulSoup(page.content(), 'html.parser')
        clean_data = fetch_data(page)
        manager.save_to_excel(clean_data)
