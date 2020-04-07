from nameko import config

from tweets.dependencies import receive


class TweetService:
    name = "tweets_service"

    @receive(
        wait_for=int(config["TIMELINE_INTERVAL"]), days_back=int(config["TIMELINE_DAYS_BACK"])
    )
    def handle_timeline_message(self, body):
        print("I have got a new favorited tweet")
        print(body)
