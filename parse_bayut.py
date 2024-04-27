import time
from random import randint
from playwright.sync_api import sync_playwright
import requests
from bs4 import BeautifulSoup
from to_exel import ExcelManager


manager = ExcelManager('test_3.xlsx', ['title', 'location', 'city', 'bath', 'bed', 'area', 'price'])


with sync_playwright() as p:
    browser = p.firefox.launch(headless=False,timeout=9000000)
    context = browser.new_context()
    page = context.new_page()
    for _ in range(2, 432):
        data = []
        url = f'https://www.bayut.com/for-sale/property/dubai/dubai-marina/page-{_}/?locations=%2Fdubai%2Fjumeirah-lake-towers-jlt%2C%2Fdubai%2Fjumeirah-beach-residence-jbr%2C%2Fdubai%2Fbusiness-bay'
        page.goto(url, timeout=9000000)
        prices = page.query_selector_all('span[aria-label="Price"]')
        titles = page.query_selector_all('h2[aria-label="Title"]')
        locations = page.query_selector_all('div[aria-label="Location"]')
        baths = page.query_selector_all('//span[@aria-label="Studio" or @aria-label="Baths" ]')
        beds = page.query_selector_all('span[aria-label="Beds"]')
        areas = page.query_selector_all('span[aria-label="Area"]')
        print(_, url)
        for price, title, location, bath, bed, area in zip(prices, titles, locations, baths, beds, areas):
            city = location.text_content().split(', ')[-1]
            data.append([
                title.text_content(),
                location.text_content(),
                city,
                bath.text_content(),
                bed.text_content(),
                area.text_content(),
                price.text_content()
            ])
        manager.save_to_excel(data)







