from rest_framework import serializers

from tweetmarks.tweets.models import Tweet


class TweetCreateSerializer(serializers.ModelSerializer):
    """Create-only serializer for Tweet model."""

    class Meta:
        model = Tweet
        fields = ('link_url', 'posted_at', 'posted_by', 'text', 'ref_id')


class TweetReadOnlySerializer(serializers.BaseSerializer):

    def to_representation(self, obj):
        return {
            'link_url': obj.link_url,
            'posted_at': obj.posted_at,
            'posted_by': obj.posted_by,
            'text': obj.text,
            'ref_id': obj.ref_id,
            'created_at': obj.created_at,
        }
