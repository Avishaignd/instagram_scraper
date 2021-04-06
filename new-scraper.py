from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time
import re
from urllib.request import urlopen
import json
from pandas.io.json import json_normalize
import pandas as pd, numpy as np
import ast
from datetime import datetime

email = '' # logging user email
password = '' # logging user password
username='' # user to scrape
browser = webdriver.Chrome()
links=[]
all_posts = []

def login(email, password):
    browser.get('https://www.instagram.com/'+username+'/?hl=en')
    time.sleep(5)
    browser.find_element_by_name("username").send_keys(email)
    browser.find_element_by_name("password").send_keys(password)
    browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div').click()
    time.sleep(5)
    browser.get('https://www.instagram.com/'+username+'/?hl=en')
    time.sleep(5)

def scroll_page(driver, timeout):
    scroll_pause_time = timeout
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        source = browser.page_source
        data=bs(source, 'html.parser')
        body = data.find('body')
        script = body.find('script', text=lambda t: t.startswith('window._sharedData'))
        page_json = script.string.split('=', 1)[1].rstrip(';')
        data = json.loads(page_json)
        for link in data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']:
            links.append(link)
            # print(link)
            # if not any(post['node']['id'] == link['node']['id'] for post in links):

        # Wait to load page
        time.sleep(scroll_pause_time)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            # If heights are the same it will exit the function
            break
        last_height = new_height


# Pagelength = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

#Extract links from user profile page
def get_data():
    login()
    scroll_page(browser, 5)
    for item in links:
        post_dict = {
        'type': '',
        'creative': '',
        'caption': '',
        'comments': '',
        'likes': 0,
        'shares': 0,
        'views': 0,
        'all-engagement': 0,
        'date': '',
        'thumbnail': '',
        'id': ''
        }
        post_dict['id'] = item['node']['id']

        if len(item['node']['edge_media_to_caption']['edges']) > 0:
            post_dict['caption'] = item['node']['edge_media_to_caption']['edges'][0]['node']['text']
        else:
            post_dict['caption'] = 'no caption'
        
        if item['node']['is_video'] == False:
            post_dict['type'] = 'image'
        else:
            post_dict['type'] = 'video'
            post_dict['thumbnail'] = item['node']['thumbnail_src']
            post_dict['views'] = item['node']['video_view_count']

        post_dict['comments'] = item['node']['edge_media_to_comment']['count']
        post_dict['date'] = datetime.fromtimestamp(item['node']['taken_at_timestamp'])
        post_dict['creative'] = item['node']['display_url']
        post_dict['likes'] = item['node']['edge_media_preview_like']['count']
        post_dict['all-engagement'] = post_dict['comments'] + post_dict['likes'] + post_dict['views']
        all_posts.append(post_dict)
        print(all_posts)
        print(len(all_posts))


get_data()