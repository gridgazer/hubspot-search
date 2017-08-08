#!/usr/local/bin/python

import json
import requests
import pastel
import collections
from algoliasearch import algoliasearch
from HTMLParser import HTMLParser
from requests.exceptions import ConnectionError
from os import environ
import sys
reload(sys)

# --- algolia config and init
algolia_app_id            = environ['algolia_app_id']
algoia_api_key            = environ['algoia_api_key']
algolia_index             = "docs"
# --- end algolia init

# --- hubspot init
hubspot_api_key           = environ['hubspot_api_key']
# hubspot_blog_id is used as content_group_id from the hubspot api
#   api ref: https://developers.hubspot.com/docs/methods/blogv2/get_blog_posts
#
# the content_group_id can be found in the hubspot dashboard url:
#   https://app.hubspot.com/blog-beta/:portal_id/blogs/:content_group_id/manage/posts/all
hubspot_blog_id           = environ['hubspot_blog_id']
hubspot_api_params        = "&state=PUBLISHED&limit=500&content_group_id=" # If you want/need to pass any additional HubSpot blog post API params
hubspot_blog_api_base_url = "https://api.hubapi.com/content/api/v2/blog-posts?hapikey="
hubspot_post_params       = ['url','name','post_summary','post_body','meta_description','created','featured_image']
# --- end hubsiot init

class MarkupStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    parser       = HTMLParser()
    html         = parser.unescape(html)
    s            = MarkupStripper()
    s.feed(html)
    return s.get_data()

def update_index (payload):
    print (pastel.colorize('<fg=blue>updating index on algolia...\n</>'))
    algolia_index.add_objects(payload)

try:
    sys.setdefaultencoding('utf-8')
    algolia_client = algoliasearch.Client(algolia_app_id, algoia_api_key)
    algolia_index  = algolia_client.init_index(algolia_index)
    api_response   = requests.get(hubspot_blog_api_base_url + hubspot_api_key + hubspot_api_params + hubspot_blog_id)
    blog_data      = api_response.json()
    for post in blog_data['objects']:
        print (pastel.colorize('<fg=red>dealing with post titled: ' + post['html_title']))
        batch = []
        segment = collections.OrderedDict()
        for key in post.items():
            segment["objectID"] = post['id']
            if key[0] in hubspot_post_params:
                    if type(key[1]) is not int:
                        segment[key[0]] = str(strip_tags(key[1]))
                        # segment[key[0]] = str(key[1])
                    else:
                        segment[key[0]] = key[1]
        batch.append(segment)
        update_index(batch)
    print (pastel.colorize('<fg=white;bg=blue;options=bold>Done processing ' + str(len(blog_data['objects'])) + ' posts!</>\n'))

except requests.exceptions.RequestException as e:
    print (pastel.colorize('<fg=yellow;bg=red;options=bold>Connection error while making API call to HubSpot! ' + e + ' Aborted.</>\n'))
    sys.exit(1)
