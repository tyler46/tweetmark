from datetime import datetime

from nameko.rpc import rpc, RpcProxy
import requests
from requests.exceptions import ConnectionError, RequestException
from requests.status_codes import codes

import config

VALID_STATUS_CODES = (
    codes.ok,  # 200
    codes.created,  # 201
    codes.no_content,  # 204
)

TWITTER_DATETIME_FORMAT = '%a %b %d %H:%M:%S %z %Y'
FAVORITE = 'favorite'


def extract_url(entities):
    return [item['expanded_url'] for item in entities['urls']][0]


def get_twitter_public_url(screen_name):
    return 'https://twitter.com/{}'.format(screen_name)


class StoreTweetService:

    name = 'store_tweet_service'

    @rpc
    def send_payload(self, payload):
        url = config.API_URL
        try:
            # TODO: Add some custom authorization header
            # for somekind of security
            response = requests.post(url, json=payload)
            if response.status_code not in VALID_STATUS_CODES:
                print('error, invalid status code: {}'.format(response.status_code))
                print('reason: {}'.format(response.content))
        except (RequestException, ConnectionError) as exc:
            print('error')


class FavoritedTweetService:

    name = 'tweet_favorites_service'

    api = RpcProxy('store_tweet_service')

    @rpc
    def process_tweet(self, user, tweet, action):
        print('{0} has favorited the following tweet: {1}'.format(user, tweet))
        if action != FAVORITE:
            # self.api.delete_resource(tweet['id_str'])
            print('Unvaforited')
        else:
            posted_at = datetime.strptime(tweet['created_at'], TWITTER_DATETIME_FORMAT)
            data = {
                'link_url': extract_url(tweet['entities']),
                'posted_at': posted_at.isoformat(),
                'posted_by': get_twitter_public_url(tweet['user']['screen_name']),
                'text': tweet['text'],
                'public_id': tweet['id_str']
            }
            self.api.send_payload(data)
