from django.db import models

from taggit.managers import TaggableManager


class Tweet(models.Model):
    """Tweet mode definition."""

    link_url = models.URLField()
    posted_at = models.DateTimeField()
    posted_by = models.CharField(max_length=150)
    text = models.TextField()
    ref_id = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager()
