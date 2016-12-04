from rest_framework import generics, mixins, viewsets

from tweetmarks.tweets.api.serializers import (
    TweetCreateSerializer, TweetReadOnlySerializer
)
from tweetmarks.tweets.models import Tweet


class TweetCreateDestroyView(mixins.CreateModelMixin,
                             mixins.DestroyModelMixin,
                             viewsets.GenericViewSet):
    """Create-destroy endpoint to add a newly favorited
    tweet or deleting an existing one.
    """
    queryset = Tweet.objects.all()
    serializer_class = TweetCreateSerializer
    lookup_field = 'ref_id'


class TweetListView(generics.ListAPIView):
    """List-only endpoint to list tweets."""

    queryset = Tweet.objects.all()
    serializer_class = TweetReadOnlySerializer
