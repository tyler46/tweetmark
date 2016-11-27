import json
import logging

from tweepy.models import Status
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
import tweepy

from nameko.standalone.rpc import ClusterRpcProxy


import settings

FAVORITE = 'favorite'


def setup_twitter_auth():
    auth = OAuthHandler(consumer_key=settings.CONSUMER_KEY,
                        consumer_secret=settings.CONSUMER_SECRET)

    auth.set_access_token(settings.ACCESS_TOKEN,
                          settings.ACCESS_TOKEN_SECRET)

    return auth


class FavoritedTweetsListener(StreamListener):
    """Stream listener that process only tweets that
    got favorited from authenticated user.
    """

    def on_connect(self):
        """Called once connected to streaming server.

        This will be invoked once a successful response
        is received from the server. Allows the listener
        to perform some work prior to entering the read loop.
        """
        self.theuser = self.api.me()
        print('API User: {}'.format(self.theuser))
        # using option 'a' for appending new entry to file.
        self.fav_marks = open(settings.FAVORITES_FILE, 'a')

    def on_data(self, raw_data):
        self.fav_marks.write(raw_data)
        data = json.loads(raw_data)

        if 'event' in data:
            status = Status.parse(self.api, data)
            if self.on_event(status) is False:
                return False
        elif 'limit' in data:
            if self.on_limit(data['limit']['track']) is False:
                return False
        elif 'disconnect' in data:
            if self.on_disconnect(data['disconnect']) is False:
                return False
        elif 'warning' in data:
            if self.on_warning(data['warning']) is False:
                return False
        else:
            logging.debug("message type: " + str(raw_data))

    def on_exception(self, exception):
        """Called when an unhandled exception occurs."""
        return

    def on_event(self, status):
        """Called when a new event arrives"""
        if status.source['id'] == self.theuser.id:
            with ClusterRpcProxy(settings.RPC_CONFIG) as rpc:
                rpc.tweet_favorites_service.process_tweet.call_async(
                        status.source, status.target_object, status.event)

        return

    def on_limit(self, track):
        """Called when a limitation notice arrives"""
        return

    def on_error(self, status_code):
        """Called when a non-200 status code is returned"""
        return False

    def on_timeout(self):
        """Called when stream connection times out"""
        return

    def on_disconnect(self, notice):
        """Called when twitter sends a disconnect notice

        Disconnect codes are listed here:
        https://dev.twitter.com/docs/streaming-apis/messages#Disconnect_messages_disconnect
        """
        return

    def on_warning(self, notice):
        """Called when a disconnection warning message arrives"""
        return


if __name__ == '__main__':
    try:
        auth = setup_twitter_auth()
        api = tweepy.API(auth)

        # Create the listener
        listener = FavoritedTweetsListener(api=api)
        stream = tweepy.Stream(auth, listener)

        authenticated_username = auth.get_username()

        stream.userstream(_with=[authenticated_username])
    except KeyboardInterrupt:
        logging.info('exiting')
        stream.disconnect()
        pass
    finally:
        listener.fav_marks.close()




#   public_tweets = api.home_timeline()
#   for tweet in public_tweets:
#       print(tweet.text)
