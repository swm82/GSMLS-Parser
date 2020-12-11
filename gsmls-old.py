from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import sys
import pickle
import re


class Property:
    def __init__(self, address, price, mlsnumber):
        self.address = address
        self.price = price
        self.mlsnumber = mlsnumber

    def __str__(self):
        return self.address + " - " + "${:,.2f}".format(self.price)

def export_properties(properties):
    output = open("test", 'wb')
    pickle.dump(properties, output)
    output.close()

def import_properties():
    input = open("test", 'rb')
    properties = pickle.load(input)
    input.close()
    return properties

def get_dropped_listings(current_data, new_data):
    dropped_listing = []
    for current_property in current_data:
        if new_data.get(current_property) is None:
            dropped_listing.append(current_data[current_property])

    return dropped_listing

def get_new_listings(current_data, new_data):
    new_listing = []
    for new_property in new_data:
        if current_data.get(new_property) is None:
            new_listing.append(new_data[new_property])
    return new_listing

def get_price_changes(current_data, new_data):
    price_changes = []
    for mlsnum, property in current_data.items():
        if new_data.get(mlsnum) is not None:
            if new_data.get(mlsnum).price != property.price:
                price_changes.append(new_data.get(mlsnum))
    return price_changes



def parse_data(county, town, maxPrice):
    browser = webdriver.Firefox(executable_path=r'/usr/local/bin/geckodriver')
    browser.get('http://gsmls.com')
    elem = browser.find_element_by_css_selector('#content > div.content-right-corner2 > div > div > div > div.w69p.l.padb10 > div > div > div > div > div > p > a > img')
    elem.click()
    # Select County
    select = Select(browser.find_element_by_css_selector('#countycode'))
    select.select_by_visible_text(county)
    elem = browser.find_element_by_css_selector('.marl125 > button:nth-child(1) > img:nth-child(1)')
    elem.click()

    # Select town
    select = Select(browser.find_element_by_css_selector('#town'))
    select.deselect_all()
    select.select_by_visible_text(town)
    elem = browser.find_element_by_css_selector('.w69p > p:nth-child(2) > button:nth-child(2) > img:nth-child(1)')
    elem.click()

    # Select Min/Max
    select = Select(browser.find_element_by_css_selector('#minlistprice'))
    select.select_by_visible_text("$0")
    select = Select(browser.find_element_by_css_selector('#maxlistprice'))
    select.select_by_visible_text("$" + maxPrice)
    #Search
    elem = browser.find_element_by_css_selector('.center > button:nth-child(2) > img:nth-child(1)')
    elem.click()

    # Get addresses
    addresses = browser.find_elements_by_class_name('address')
    #Get prices
    prices = browser.find_elements_by_css_selector('div.formline140.floatholder > p')

    #Get MLS numbers
    mlsnum = []
    for i in range(2, 2 * len(addresses) + 1, 2):
        selector = f'#propsearch > div.bufer > div > div:nth-child({i}) > div:nth-child(2) > div > div:nth-child(1)'
        element = browser.find_elements_by_css_selector(selector)
        mlsnumber = int(re.search("\d+", element[0].text).group())
        mlsnum.append(mlsnumber)

    #Print data
    properties = {}

    for i in range(len(addresses)):
        price = int(''.join(re.findall("\d+", prices[i].text)))
        property = Property(addresses[i].text, price, mlsnum[i])
        properties[mlsnum[i]] = property

    browser.close()
    return properties

county = sys.argv[1]
town = sys.argv[2]
maxPrice = sys.argv[3]

# import previously seen properties
curr_properties = import_properties()

# parse data on GSMLS
new_properties = parse_data(county, town, maxPrice)

# print all properties
for key, value in new_properties.items():
    print(str(key) + " - " + value.address)

# find new listings
new_listings = get_new_listings(curr_properties, new_properties)
print("NEW LISTINGS")
for x in new_listings:
    print(x.address)

# check for properties removed from gsmls
dropped_listings = get_dropped_listings(curr_properties, new_properties)
print("REMOVED LISTINGS")
for x in dropped_listings:
    print(x.address)

# check for price changes
new_prices = get_price_changes(curr_properties, curr_properties)
print("PRICE CHANGES:")
for x in new_prices:
    print(x)

result = input("Export updated listings? Y/N: ")
if result.lower() == 'y':
    export_properties(new_properties)
    print("updated...")


# TODO
# catch errors in input town/county, max price
# match objects, - if new - create new, alert to new properties
# match objects - if price change alert
# define stuff as methods
# save to file/read from file (pickle?)
# use classes for town objects to save different lists of houses
# implement switch to select town/county
# remove non existing listings
# add time of first parse
