from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import urllib.request
import time
import os

# TODO
print("Bing search not implemented!")

search_engine = int(input("[1] Google\n[2] DuckDuckGo\n[3] Bing\n>: "))
query = input("Search query: ")
limit = int(input("Enter the required no. of pics: "))

browser = webdriver.Firefox()

if search_engine == 1:
    browser.get('https://www.google.com/')

    image_link = browser.find_element(by=By.LINK_TEXT, value='Images')
    image_link.get_attribute('href')
    image_link.click()

    search = browser.find_element(by=By.NAME, value='q')
    search.send_keys(query, Keys.ENTER)

else:
    browser.get('https://duckduckgo.com/?q=')

    search = browser.find_element(by=By.ID, value="search_form_input_homepage")
    search.get_attribute('href')
    search.click()

    search.send_keys(query, Keys.ENTER)
    browser.implicitly_wait(2)

    image_link = browser.find_element(by=By.PARTIAL_LINK_TEXT, value="Images")
    image_link.get_attribute('href')
    image_link.click()

value = 0
for i in range(10):
    browser.execute_script("scrollBy(" + str(value) + ",+1000);")
    value += 1000
    time.sleep(0.1)

if search_engine == 1:
    screen_ = browser.find_element(by=By.ID, value="islmp")
    image_ = screen_.find_elements(by=By.TAG_NAME, value='img')
else:
    screen_ = browser.find_element(by=By.ID, value="zero_click_wrapper")
    image_ = screen_.find_elements(by=By.TAG_NAME, value='img')

current = 0
counter = 0

try:
    os.mkdir(query)
except Exception as p:
    print(p, "\nOverwriting")

count = 0
for i in image_:
    src = i.get_attribute('src')
    count += 1
    if count > limit:
        break
    if src:
        src = str(src)
        print("Downloaded image: ", count)
        try:
            urllib.request.urlretrieve(src, os.path.join(f'{query}', 'image' + str(count) + '.jpg'))
        except Exception:
            count -= 1
            print(f'Could not print image: {count}\n')
    else:
        count -= 1
        print(f'Could not print image: {count}\n')

print("Total images downloaded: ", (count - 1))

browser.close()
