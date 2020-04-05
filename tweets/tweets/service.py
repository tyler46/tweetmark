from tweets.dependencies import receive


class TweetService:
    name = "tweets_service"

    @receive(wait_for=60, days_back=15)
    def handle_timeline_message(self, body):
        print("I have got a new favorited tweet")
        print(body)
