import logging

import arrow
import tweepy
from eventlet import sleep
from nameko.exceptions import ConfigurationError
from nameko.extensions import Entrypoint

from tweets import constants

TWITTER_DATE_TIME_FORMAT_STRING = "ddd MMM DD HH:mm:ss Z YYYY"


log = logging.getLogger(__name__)


class TwitterClient:
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        self.auth = self.auth = tweepy.OAuthHandler(
            consumer_key=consumer_key, consumer_secret=consumer_secret,
        )
        self.auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(self.auth)

    def receive_favorites(self, page):
        me = self.api.me()
        return self.api.favorites(id=me.id, page=page)


class TwitterFavoritesReceive(Entrypoint):
    """
    Twitter Favorites entrypoint.
    """

    def __init__(self, wait_for, days_back, **kwargs):
        """Initialize the entrypoint

        Args:
            wait_for (int): Interval wait until next fetch fires.
            days_back (int): How old tweets to process.
        """
        self.wait_for = wait_for
        self.days_back = days_back

        self.client = None
        self._thread = None
        super().__init__(**kwargs)

    def setup(self):
        try:
            config = self.container.config[constants.TWITTER_CONFIG_KEY]
        except KeyError:
            raise ConfigurationError(f"`{constants.TWITTER_CONFIG_KEY}` config key not found.")

        try:
            consumer_key = config[constants.TW_CONSUMER_KEY]
            consumer_secret = config[constants.TW_CONSUMER_SECRET]
            access_token = config[constants.TW_ACCESS_TOKEN]
            access_token_secret = config[constants.TW_ACCESS_TOKEN_SECRET]
        except KeyError as exc:
            raise ConfigurationError(
                f"`{constants.TWITTER_CONFIG_KEY}` configuration does not contain "
                f"mandatory {exc.args[0]} key."
            )
        self.client = TwitterClient(
            consumer_key, consumer_secret, access_token, access_token_secret
        )

        super().setup()

    def start(self):
        self._thread = self.container.spawn_managed_thread(
            self.run, identifier="TwitterFavoritesReceiver.run"
        )
        super().start()
        log.debug(f"{self} started")

    def stop(self):
        self._kill_thread()
        super().stop()
        log.debug(f"{self} stopped")

    def kill(self):
        self._kill_thread()
        super().kill()
        log.debug(f"{self} killed")

    def run(self):
        utcnow = arrow.utcnow()
        days_back_threshold = utcnow.shift(days=-self.days_back)
        try:
            while True:

                page = 0
                keep_running = True

                while keep_running:
                    page += 1
                    for status in self.client.receive_favorites(page):
                        tweet_created_at = arrow.get(
                            status._json["created_at"], TWITTER_DATE_TIME_FORMAT_STRING
                        )
                        if tweet_created_at.date() >= days_back_threshold.date():
                            self.handle_status(status)
                        else:
                            # Outside given window, break for-loop and break while-loop too.
                            keep_running = False
                            break

                sleep(self.wait_for)
        finally:
            log.info("Stopped receiving twitter favorites")

    def handle_status(self, status):
        args = [status._json]
        kwargs = {}
        self.container.spawn_worker(self, args, kwargs)

    def _kill_thread(self):
        if self._thread is not None:
            self._thread.kill()


receive = TwitterFavoritesReceive.decorator
