import requests
from bs4 import BeautifulSoup
import time
import json

# Scrapes county and town codes from GSML - delay optional
def get_codes():
    # Get county codes
    url = 'https://www2.gsmls.com/publicsite/getcountysearch.do?method=getcountysearch&bundle=publicsite.English'
    response = requests.request('GET', url)
    soup = BeautifulSoup(response.text, 'html.parser')
    counties = {
        item.string.strip(): {
            'code': int(item['value'])
        }
        for item in soup.find_all('option')
    }

    for county in sorted(counties.keys()):
        # Get town codes
        url = f'https://www2.gsmls.com/publicsite/getcommsearch.do?method=getcommsearch&county={counties[county]["code"]}'
        response = requests.request('GET', url)
        soup = BeautifulSoup(response.text, 'html.parser')
        towns = {
            item.string.strip(): int(item['value'])
            for item in soup.find_all('option')[6:]
        }
        counties[county]['towns'] = towns
        #time.sleep(1)
    with open('county_codes.json', 'w') as f:
        json.dump(counties, f)
    return(counties)
