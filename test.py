import requests
import json
import time

# Variables
LOGIN_URL = 'https://www.instagram.com/accounts/login/ajax/'
REFERER_URL = 'https://www.instagram.com/accounts/login/'
USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'
USERNAME = 'avishaignd'
PASSWD = '1pass4instagram'
IGQ = r"https://www.instagram.com/graphql/query/?query_hash=58712303d941c6855d4e888c5f0cd22f&variables=%7B%22id%22%3A%2225025320%22%2C%22first%22%3A24%7D"

# Session variables
session = requests.session()
req = session.get(LOGIN_URL)
session.headers = {'user-agent': USER_AGENT}
session.headers.update({'Referer': REFERER_URL})
session.headers = {'user-agent': USER_AGENT}
session.headers.update({'x-csrftoken': req.cookies['csrftoken']})
login_data = {'username': USERNAME, 'password': PASSWD}
login = session.post(LOGIN_URL, data=login_data, allow_redirects=True)
session.headers.update({'x-csrftoken': login.cookies['csrftoken']})

# Parse followings
def parse():
    try:
        following = session.get(IGQ)
        test_text = json.loads(following.text)
        usernames = []

        j = test_text['data']['user']['edge_follow']
        for each in j['edges']:
            usernames.append(each['node']['username'])
        print(usernames)

    except:
        print("Couldn't login.")
parse()