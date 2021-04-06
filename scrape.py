import json
from datetime import datetime

f = open("pudding.json", "r", encoding="utf8")
data = f.read()
my_json = json.loads(data)
all_page_data = []

posts_list = my_json['data']['user']['edge_owner_to_timeline_media']['edges']
for item in posts_list:
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
    all_page_data.append(post_dict)

print(all_page_data)