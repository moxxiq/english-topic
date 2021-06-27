from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
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


def topic(request, topic_id):
    try:
        topic_details = Topic.objects.get(id=topic_id)
    except Topic.DoesNotExist:
        raise Http404("Topic does not exist")
    upvotes = Count(F('vote_value'), filter=Q(vote_value=Vote.VoteEnum.UPVOTE))
    downvotes = Count(F('vote_value'), filter=Q(vote_value=Vote.VoteEnum.DOWNVOTE))
    rating_list = Vote.objects.filter(id=topic_id).annotate(
        upvotes=upvotes,
        downvotes=downvotes,
        offset=upvotes - downvotes,
    )
    rating = rating_list[0].offset if len(rating_list) > 0 else 0
    return render(request, 'topics/topic.html',
                  {"topic": topic_details,
                   "rating": rating,
                   })
