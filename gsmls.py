from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import sys


class Property:
    def __init__(self, address, price):
        self.address = address
        self.price = price

county = sys.argv[1]
town = sys.argv[2]
maxPrice = sys.argv[3]


browser = webdriver.Firefox(executable_path=r'/usr/local/bin/geckodriver')
browser.get('http://gsmls.com')
elem = browser.find_element_by_css_selector('#content > div.content-right-corner2 > div > div > div > div.w69p.l.padb10 > div > div > div > div > div > p > a > img')
elem.click()
# Select County
select = Select(browser.find_element_by_css_selector('#countycode'))
select.select_by_visible_text("county")
elem = browser.find_element_by_css_selector('.marl125 > button:nth-child(1) > img:nth-child(1)')
elem.click()

# Select town
select = Select(browser.find_element_by_css_selector('#town'))
select.deselect_all()
select.select_by_visible_text("town")
elem = browser.find_element_by_css_selector('.w69p > p:nth-child(2) > button:nth-child(2) > img:nth-child(1)')
elem.click()

# Select Min/Max
select = Select(browser.find_element_by_css_selector('#minlistprice'))
select.select_by_visible_text("$0")
select = Select(browser.find_element_by_css_selector('#maxlistprice'))
select.select_by_visible_text(maxPrice)
#Search
elem = browser.find_element_by_css_selector('.center > button:nth-child(2) > img:nth-child(1)')
elem.click()

# Get addresses
addys = browser.find_elements_by_class_name('address')
#Get prices
prices = browser.find_elements_by_css_selector('div.formline140.floatholder > p')

#Get MLS numbers
mlsnum = []
for i in range(2, 2 * len(addys) + 1, 2):
    selector = f'#propsearch > div.bufer > div > div:nth-child({i}) > div:nth-child(2) > div > div:nth-child(1)'
    element = browser.find_elements_by_css_selector(selector)
    mlsnum.append(element[0].text)

#Print data
for i in range(len(addys)):
    print(addys[i].text)
    print(prices[i].text)
    print(mlsnum[i])

browser.close()

# TODO
# catch errors in input town/county, max price
# sort the list
# implement properties as objects
# match objects, - if new - create new, alert to new properties
# match objects - if price change alert
# define stuff as methods
# save to file/read from file (pickle?)
# use classes for town objects to save different lists of houses