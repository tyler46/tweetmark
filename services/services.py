from nameko.rpc import rpc


def extract_urls(entities):
    return [item['expanded_url'] for item in entities['urls']]


def get_twitter_public_url(screen_name):
    return 'https://twitter.com/{}'.format(screen_name)


class FavoritedTweetService:

    name = 'tweet_favorites_service'

    @rpc
    def process_tweet(self, user, tweet):
        print('{0} has favorited the following tweet: {1}'.format(user, tweet))

        return {
            'user': user['screen_name'],
            'fav': tweet['text']
        }
