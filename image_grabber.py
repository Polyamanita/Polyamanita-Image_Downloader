from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import urllib.request
import shutil
import time
import csv
import os

# TODO
print("Bing search not implemented!")

csv_file_name = 'florida_mushi.csv'

google = False
duckduckgo = True

smallest_csv_count = 250  # smallest amount of instances, last column in the csv file; i.e. 25

limit = 5  # number of images you may download; i.e. 125
smallest_allowed = 5  # smallest amount of images you're allowed to download w/o being useless; i.e. 50

try:
    os.mkdir("images")
except Exception as p:
    print(p, "\nOverwriting")

browser = webdriver.Firefox()
error_log = open('error.log', 'a')
error_log.truncate(0)
error_log.write("error-type, query\n")

global_start_time = time.time()
local_total_time_array = list()

total_count = 0
search_engine = 1

if google:
    with open(csv_file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0

        search_engine_name = 'google'
        print(f"\nUsing search engine: {search_engine_name}")

        browser.get('https://www.google.com/')
        image_link = browser.find_element(by=By.LINK_TEXT, value='Images')
        image_link.get_attribute('href')
        image_link.click()

        search = browser.find_element(by=By.NAME, value='q')

        for row in csv_reader:

            if line_count == 0:
                line_count += 1
                continue
            elif int(row[3]) < smallest_csv_count:
                continue
            else:
                query = row[1] + ' ' + row[2]
                print(f"\n\nQuery: {query}")

                try:
                    os.mkdir("images/" + query)
                except Exception as p:
                    print(p, "\nOverwriting")

                local_start_time = time.time()

                query_pedantic = '\"' + query + '\"'
                search = browser.find_element(by=By.NAME, value='q')
                search.clear()
                search.send_keys(query_pedantic, Keys.ENTER)

                value = 0
                for i in range(10):
                    browser.execute_script("scrollBy(" + str(value) + ",+1000);")
                    value += 1000
                    time.sleep(0.1)

                try:
                    screen_ = browser.find_element(by=By.ID, value="islmp")
                    image_ = screen_.find_elements(by=By.TAG_NAME, value='img')
                except Exception as p:
                    print(p, f"Failed at grabbing webpage on query: {query}")
                    search_engine += 1
                    continue

                current = 0
                counter = 0

                query_path = "images/" + query + '/' + search_engine_name

                try:
                    os.mkdir(query_path)
                except Exception as p:
                    print(p, f"Error making {query_path}")

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
                            urllib.request.urlretrieve(src,
                                                       os.path.join(f'{query_path}', 'image' + str(count) + '.jpg'))
                        except Exception as p:
                            count -= 1
                            print(p, f'Could not print image: {count}\n')
                    else:
                        count -= 1
                        print(f'Could not print image: {count}\n')

                try:
                    if count < smallest_allowed:
                        error_log.write(f"SMALL IMAGE COUNT, {query}\n")
                        shutil.rmtree(query_path)
                        print(f"Deleted useless query \"{query_path}\"")
                        count = 0
                    # else:
                    #    print("Total images downloaded: ", (count - 1))
                except Exception as p:
                    print(p, f"\nFailed to delete useless folder \"{query_path}\"")
                    count = 0

                if count != 0:
                    total_count += count - 1

                local_total_time_array.append(time.time() - local_start_time)
                line_count += 1
        print(f'\n\nProcessed {line_count} lines of the .csv file!')
        csv_file.close()

if duckduckgo:
    with open(csv_file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0

        browser.get('https://duckduckgo.com/?q=')

        search = browser.find_element(by=By.ID, value="search_form_input_homepage")
        search.get_attribute('href')
        search.click()

        search.send_keys(".", Keys.ENTER)
        browser.implicitly_wait(2)

        image_link = browser.find_element(by=By.PARTIAL_LINK_TEXT, value="Images")
        image_link.get_attribute('href')
        image_link.click()

        for row in csv_reader:

            if line_count == 0:
                line_count += 1
                continue
            elif int(row[3]) < smallest_csv_count:
                continue
            else:
                query = row[1] + ' ' + row[2]
                print(f"\n\nQuery: {query}")

                try:
                    os.mkdir("images/" + query)
                except Exception as p:
                    print(p, "\nOverwriting")

                local_start_time = time.time()

                search_engine_name = 'duckduckgo'

                print(f"\nUsing search engine: {search_engine_name}")

                query_pedantic = '\"' + query + '\"'
                search = browser.find_element(by=By.ID, value="search_form_input")
                # TODO, this does not work on duckduckgo?
                # search.clear()
                search.send_keys(query_pedantic, Keys.ENTER)

                value = 0
                for i in range(10):
                    browser.execute_script("scrollBy(" + str(value) + ",+1000);")
                    value += 1000
                    time.sleep(0.1)

                try:
                    screen_ = browser.find_element(by=By.ID, value="zero_click_wrapper")
                    image_ = screen_.find_elements(by=By.TAG_NAME, value='img')
                except Exception as p:
                    print(p, f"Failed at grabbing webpage on query: {query}")
                    search_engine += 1
                    continue

                current = 0
                counter = 0

                query_path = "images/" + query + '/' + search_engine_name

                try:
                    os.mkdir(query_path)
                except Exception as p:
                    print(p, f"Error making {query_path}")

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
                            urllib.request.urlretrieve(src,
                                                       os.path.join(f'{query_path}', 'image' + str(count) + '.jpg'))
                        except Exception as p:
                            count -= 1
                            print(p, f'Could not print image: {count}\n')
                    else:
                        count -= 1
                        print(f'Could not print image: {count}\n')

                try:
                    if count < smallest_allowed:
                        error_log.write(f"SMALL IMAGE COUNT, {query}\n")
                        shutil.rmtree(query_path)
                        print(f"Deleted useless query \"{query_path}\"")
                        count = 0
                    # else:
                    #    print("Total images downloaded: ", (count - 1))
                except Exception as p:
                    print(p, f"\nFailed to delete useless folder \"{query_path}\"")
                    count = 0

                if count != 0:
                    total_count += count - 1

                local_total_time_array.append(time.time() - local_start_time)
                # print(f"Finished in: {time.time() - local_start_time}")
                line_count += 1
        print(f'\n\nProcessed {line_count} lines of the .csv file!')

    csv_file.close()

avg_time = sum(local_total_time_array) / len(local_total_time_array)
global_time = time.time() - global_start_time

print(f"Total images downloaded: {total_count}")
print(f"Average search time execution: {round(avg_time,2)}")
print(f"Global time execution: {round(global_time, 2)}")

error_log.close()
browser.close()
