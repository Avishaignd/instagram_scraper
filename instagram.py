import json
import requests
import ast
from proxy_requests.proxy_requests import ProxyRequests
from selenium import webdriver
from fake_headers import Headers

# driver = webdriver.Chrome()

if __name__ == "__main__":
    header = Headers(
        browser="chrome",  # Generate only Chrome UA
        os="win",  # Generate ony Windows platform
        headers=True  # generate misc headers
    )


def site_login():
    driver.get ('https://www.instagram.com/graphql/query/?query_hash=003056d32c2554def87228bc3fd9668a&id=214535086&first=100')
    driver.find_element_by_name("username").send_keys("avishaignd@gmail.com")
    driver.find_element_by_name("password").send_keys("1pass4instagram")
    driver.find_element_by_class_name("Igw0E").click()

def getData():
    h = header.generate()
    # r = ProxyRequests("https://api.ipify.org")
    # r.get()
    url = 'https://www.instagram.com/graphql/query/?query_hash=003056d32c2554def87228bc3fd9668a&id=214535086&first=100'
    response = requests.get(url,headers=h)
    # my_json = response.content.decode('utf8').replace("'", '"')
    # my_json = response.json()
    # print(type(my_json))
    # data = ast.literal_eval(my_json)
    # s = json.dumps(data, indent=4, sort_keys=True)
    # print(type(d))
    post_list = []
    post_dict = {
        'type': '',
        'creatives': '',
        'text': '',
        'comments': '',
        'likes': 0,
        'shares': 0,
        'views': 0,
        'all-engagement': 0,
        'date': '',
        'thumbnail': ''
    }
    # print(my_json['data']['user']['edge_owner_to_timeline_media']['edges'][0]['node']['edge_media_to_caption'])
    # my_data = my_json['data']['user']['edge_owner_to_timeline_media']['edges']
    print(response.content)
    # for item in my_data:
    #     post_dict['text'] = item['node']['edge_media_to_caption']['edges']
    #     post_list.append(post_dict)
    # print(post_list)
    # print(my_json['data']['user']['edge_owner_to_timeline_media']['edges'][0])
    # print(type(my_data))

# site_login()
getData()