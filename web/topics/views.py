from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.template.defaulttags import register

from django.db.models import Count, Q, F
from .models import Topic, Vote


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def index(request):
    upvotes = Count(F('vote_value'), filter=Q(vote_value=Vote.VoteEnum.UPVOTE))
    downvotes = Count(F('vote_value'), filter=Q(vote_value=Vote.VoteEnum.DOWNVOTE))
    topic_top = Vote.objects.values('topic_id').annotate(
        upvotes=upvotes,
        downvotes=downvotes,
        offset=upvotes - downvotes,
    ).order_by('-offset')
    topic_rating = {t['topic_id']: t['offset'] for t in topic_top}
    topics_details = Topic.objects.filter(id__in=topic_rating.keys()).values()
    topics_text = {t['id']: t["topic_text"] for t in topics_details}

    template = loader.get_template('topics/index.html')
    context = {
        'top': topic_rating,
        'texts': topics_text,
    }
    return HttpResponse(template.render(context, request))
    return render(request, 'polls/index.html', context)


def topic(request, topic_id):
    return HttpResponse("You're looking at topic %s." % topic_id)
