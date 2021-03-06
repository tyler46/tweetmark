from datetime import datetime

from nameko.rpc import rpc, RpcProxy
import requests
from requests.exceptions import ConnectionError, RequestException
from requests.status_codes import codes

import settings

logger = settings.logger

VALID_STATUS_CODES = (
    codes.ok,  # 200
    codes.created,  # 201
    codes.no_content,  # 204
)

TWITTER_DATETIME_FORMAT = '%a %b %d %H:%M:%S %z %Y'
FAVORITE = 'favorite'


def extract_url(urls):
    try:
        return urls[0]['expanded_url']
    except IndexError:
        return ''


def get_twitter_public_url(screen_name):
    return 'https://twitter.com/{}'.format(screen_name)


class MailService:

    name ='mail_service'

    @rpc
    def send(self, subject, text=None):
        if text is None:
            # Mailgun requires to have a non empty text body
            text = 'No body message'

        if not settings.SEND_MAIL:
            logger.debug('Sending email with subject {0} with contents: {1}'.format(subject, text))
            return

        try:
            response = requests.post(
                settings.SANDBOX_API_URL,
                auth=('api', settings.MAILGUN_API_KEY),
                data={'from': settings.SENDER,
                    'to': [settings.RECEIVER],
                    'subject': subject,
                    'text': text})

            logger.debug(response.content)
            if response.status_code not in VALID_STATUS_CODES:
                logger.error('Unable to send email: {}'.format(response.content))
        except (RequestException, ConnectionError) as exc:
            logger.error('Unable to contact with mail service: {}'.format(exc))


class StoreTweetService:

    name = 'store_tweet_service'
    mail = RpcProxy('mail_service')

    @rpc
    def send_payload(self, payload):
        url = settings.API_URL
        try:
            # TODO: Add some custom authorization header
            # for some kind of security
            response = requests.post(url, json=payload)
            if response.status_code not in VALID_STATUS_CODES:
                subject = 'Store service error'
                text = {
                    'status': response.reason,
                    'content': response.text
                }
                self.mail.send.async(subject, text)
        except (RequestException, ConnectionError) as exc:
            subject = 'Store service connection error'
            text = exc
            self.mail.send.async(subject, text)


class FavoritedTweetService:

    name = 'tweet_favorites_service'

    api = RpcProxy('store_tweet_service')

    @rpc
    def process_tweet(self, user, tweet, action):
        if action != FAVORITE:
            # self.api.delete_resource(tweet['id_str'])
            logger.debug('Unvaforited')
        else:
            logger.debug(tweet)
            # if no url present, no reason to process
            urls = tweet['entities']['urls']
            if not urls:
                logger.debug('Ignoring tweet ...')
            else:
                posted_at = datetime.strptime(tweet['created_at'], TWITTER_DATETIME_FORMAT)
                data = {
                    'link_url': extract_url(urls),
                    'posted_at': posted_at.isoformat(),
                    'posted_by': get_twitter_public_url(tweet['user']['screen_name']),
                    'text': tweet['text'],
                    'ref_id': tweet['id_str']
                }
                self.api.send_payload.async(data)
