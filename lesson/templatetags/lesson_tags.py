from django import template
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse


register = template.Library()


@register.inclusion_tag('lesson/html_tags/card.html')
def learn_cards(request, words, lesson):
    """Пагинация"""

    paginator = Paginator(words, 1)
    page_number = request.GET.get('page', 1)

    try:
        words = paginator.page(page_number)
    except PageNotAnInteger:
        # Если page_number не целое число, то
        # выдать первую страницу
        words = paginator.page(1)
    except EmptyPage:
        # Если page_number находится вне диапазона, то
        # выдать последнюю страницу
        words = paginator.page(paginator.num_pages)
    return {'paginator_words': words}
