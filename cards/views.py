
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from cards.forms import WrongCardsForm
from cards.models import Card



from cards.utils import filter_cards


class CardDetailView(FormMixin, DetailView):
    model = Card
    template_name = 'cards/detail.html'
    success_message = 'Ваше сообщение об ошибке получено. Мы обязательно займемся этим.'
    form_class = WrongCardsForm

    def get_success_url(self):
        return reverse_lazy('card:detail', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super(CardDetailView, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return super(CardDetailView, self).form_valid(form)

    def form_valid(self, form):
        form = form.save(commit=False)
        form.author = self.request.user
        form.card = self.get_object()
        form.save()
        messages.add_message(self.request, messages.SUCCESS, self.success_message)  # Выводим сообщение
        return super(CardDetailView, self).form_valid(form)


class CardsListView(ListView):
    model = Card
    context_object_name = 'all_cards'
    template_name = 'cards/index.html'

    def get_queryset(self):
        """Переопределили queryset для поиска и сортировки"""
        query = self.request.GET.get('search')
        return filter_cards(query)


