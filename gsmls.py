import requests
from bs4 import BeautifulSoup
import time
import json
import sys
from scrapecodes import get_codes
import re

class Property:

    def __init__(self, mlsnum, address, price):
        self.mlsnum = mlsnum
        self.address = address
        self.price = price


def get_api_codes():
    try:
        with open('county_codes.json') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("It looks like you need to fetch some data to get started..")
        resp = ''
        while resp not in ['n', 'y']:
            print("Get county and town codes? Y/N")
            resp = input()
            resp = resp[0].strip().lower()
        if resp == 'n':
           sys.exit() 
        data = get_codes()
    return data

def get_input(counties):
    print('Choose a response')
    for i, county in enumerate(counties):
        print(f'[{i}] {county}')
    while True:
        choice = input()
        try:
            choice = int(choice)
        except TypeError:
            print('Invalid input')
        if choice in range(len(counties)):
            break
    return counties[choice]

def fetch_page(max_price, county_code, county_name, town_code):
    url = "https://www2.gsmls.com/publicsite/getpropertydetails.do?method=getpropertydetails"
    payload=f'idxId=&token=&minlistprice=&maxlistprice={max_price}&minbedrooms=&minbaths=&minacres=&maxacres=&lotdesc=&Search=Search&countycode={county_code}&countyname={county_name}&propertytype=RES&propertytypedesc=Residential&transactionsought=purchase&sttowns={town_code}'
    headers = {
      'Connection': 'keep-alive',
      'Cache-Control': 'max-age=0',
      'Upgrade-Insecure-Requests': '1',
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
      'Origin': 'https://www2.gsmls.com',
      'Content-Type': 'application/x-www-form-urlencoded',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
      'Sec-Fetch-Site': 'same-origin',
      'Sec-Fetch-Mode': 'navigate',
      'Sec-Fetch-User': '?1',
      'Sec-Fetch-Dest': 'document',
      'Referer': 'https://www2.gsmls.com/publicsite/getpropertysearch.do?method=getpropertysearch',
      'Accept-Language': 'en-US,en;q=0.9',
      'Cookie': 'JSESSIONID=oMUd_VvzXRQl-OYm1nFG7h-UK06dj0dik9AVpf6c.pite2; SERVERID=rtnu6'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def scrape_property_info(soup):
    property_tags = soup.findAll('div', {'class': 'w30p'})
    mlsnum_tags = soup.find_all(attrs={'name': 'selmlsnums'})
    addresses = []
    prices = []
    for i in range(0, len(property_tags), 2):
        children = property_tags[i].find_all('a', {'class': 'address'})
        for child in children:
            address = ' '.join(child.string.strip().split())
            addresses.append(address)
        children = property_tags[i].find_all('p', {'class': 'padl10'})
        for child in children:
            price = child.string.strip()
            price = int(re.sub(r"\$|,", '', price)) * 100
            prices.append(price)

    mlsnums = []
    for num in mlsnum_tags:
        z = re.search(r"\d{7}", str(num))
        mlsnums.append(int(z.group()))
    props = zip(addresses, prices, mlsnums)
    return props

if __name__ == '__main__':
    data = get_api_codes()
    county = get_input(sorted(data.keys()))
    town = get_input(sorted(data[county]['towns'].keys()))
    county_code = data[county]['code']
    town_code = data[county]['towns'][town]
    max_price = 450000
    soup = fetch_page(max_price, county_code, county, town_code)
    properties = scrape_property_info(soup)
    for prop in properties:
        print(prop)