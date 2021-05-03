from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Count, Q
from .models import Topic, Vote


def index(request):
    upvotes = Count('vote_value', filter=Q(vote_value=Vote.VoteEnum.UPVOTE))
    downvotes = Count('vote_value', filter=Q(vote_value=Vote.VoteEnum.DOWNVOTE))
    topic_top = Vote.objects.values('topic_id', 'topic__topic_text').annotate(
        upvotes=upvotes,
        downvotes=downvotes,
        offset=upvotes - downvotes,
    ).order_by('-offset')
    topics_page = '<br>'.join((f"{t['topic__topic_text']} U:{t['upvotes']} D:{t['downvotes']}" for t in topic_top))
    return HttpResponse(topics_page)


def topic(request, topic_id):
    return HttpResponse("You're looking at topic %s." % topic_id)
