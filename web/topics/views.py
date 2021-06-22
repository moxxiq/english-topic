from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Count, Q, F
from .models import Topic, Vote


def index(request):
    upvotes = Count(F('vote_value'), filter=Q(vote_value=Vote.VoteEnum.UPVOTE))
    downvotes = Count(F('vote_value'), filter=Q(vote_value=Vote.VoteEnum.DOWNVOTE))
    topic_top = Vote.objects.values('topic_id').annotate(
        upvotes=upvotes,
        downvotes=downvotes,
        offset=upvotes - downvotes,
    ).order_by('-offset')
    topic_top_dict = {t['topic_id']: {"upvotes": t['upvotes'], "downvotes": t['downvotes']} for t in topic_top}
    topics_details = Topic.objects.filter(id__in=topic_top_dict.keys()).values()
    topics_details_dict = {t['id']: {"text": t["topic_text"]} for t in topics_details}
    topics_page = '<br>'.join(f"{topics_details_dict[i]['text']} Upvotes:{topic_top_dict[i]['upvotes']} Downvotes:{topic_top_dict[i]['downvotes']}" for i in topic_top_dict.keys())
    return HttpResponse(topics_page)


def topic(request, topic_id):
    return HttpResponse("You're looking at topic %s." % topic_id)
