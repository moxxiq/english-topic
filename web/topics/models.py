from django.db import models
from django.utils.translation import gettext_lazy as _


class Topic(models.Model):
    topic_text = models.CharField(max_length=256)

    def __str__(self):
        return self.topic_text


class Vote(models.Model):

    class VoteEnum(models.IntegerChoices):
        DOWNVOTE = -1, _('Downvote')
        UPVOTE = 1, _('Upvote')
        __empty__ = _('(Unknown)')

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    vote_value = models.SmallIntegerField(choices=VoteEnum.choices)

    def __str__(self):
        return f"{self.topic} {self.get_vote_value_display()}"
