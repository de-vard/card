

from cards.models import Card
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Greatest


def filter_cards(query):
    """Функция для поиска слов"""
    if query:
        object_list = Card.objects.only('term', 'definition').annotate(
            similarity=Greatest(TrigramSimilarity('term', query), TrigramSimilarity('definition', query))
        ).filter(similarity__gt=0.1).order_by('-similarity')
    else:
        object_list = Card.objects.only('term').order_by('term')
    return object_list



