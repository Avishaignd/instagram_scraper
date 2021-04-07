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

# email = 'avishaignd@gmail.com' # logging user email
# password = '1pass4instagram' # logging user password
# username='avishaignd' # user to scrape
browser = webdriver.Chrome()


class Scraper:
    '''
    Initializing with your logging user email and password, while also setting empty lists to contain
    the posts from the page.
    The 'is_full' variable is to stop the scraping after a certain number of posts
    '''
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.links=[]
        self.is_full = False
        self.all_posts = []

    def login(self, username):
        '''
        The username variable will come from the get data function.
        The function checks if we are sent to a login page, if so it logs in, if not it goes to the next function.
        '''
        browser.get('https://www.instagram.com/'+username+'/?hl=en')
        time.sleep(5)
        try:
            browser.find_element_by_name("username").send_keys(self.email)
            browser.find_element_by_name("password").send_keys(self.password)
            browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div').click()
            time.sleep(5)
            browser.get('https://www.instagram.com/'+username+'/?hl=en')
            time.sleep(5)
        except:
            return

    def scroll_page(self, driver, timeout, number):
        '''
        Scrolling the page and parsing it, the function scrapes all posts until it reaches the desired amount.
        The function takes a few seconds between every scroll to make sure the page is loaded.
        '''
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
            while len(self.links) <= number:  
                for link in data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']:
                    self.links.append(link)
            else:
                self.is_full = True

        # Wait to load page
            time.sleep(scroll_pause_time)

        # Calculate new scroll height and compare with last scroll height, also check if there are enough posts
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height or self.is_full == True:
            # If heights are the same it will exit the function
                break
            last_height = new_height


    def get_data(self, username, number):
        '''
        In this function we pass the desired instagram username to scrape, amount of posts we want scraped,
        the timeout before each scroll (I use 5 as a default), execute the login and scrolling function, and organize the data.
        '''
        self.login(username)
        self.scroll_page(browser, 5, number)
        for item in self.links:
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
            post_dict['date'] = str(datetime.fromtimestamp(item['node']['taken_at_timestamp']))
            post_dict['creative'] = item['node']['display_url']
            post_dict['likes'] = item['node']['edge_media_preview_like']['count']
            post_dict['all-engagement'] = post_dict['comments'] + post_dict['likes'] + post_dict['views']
            self.all_posts.append(post_dict)
            print(self.all_posts)
        
        print(len(self.all_posts))
        browser.close()
