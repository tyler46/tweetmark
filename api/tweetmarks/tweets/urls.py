from django.conf.urls import url

from rest_framework.routers import DefaultRouter

from tweetmarks.tweets.api.views import TweetCreateDestroyView, TweetListView

router = DefaultRouter()
router.register(r'tweets', TweetCreateDestroyView)

urlpatterns = router.urls + [url(r'^favorites/$', TweetListView.as_view())]
