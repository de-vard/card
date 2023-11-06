from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView

from cards.forms import CardFormSet
from cards.models import Card
from courses.models import Course
from django.views.generic.edit import CreateView, UpdateView

from .forms import LessonCreationForm
from .models import Lesson, LessonProgress
from .session import LessonSession


# TODO:Всуну пока сюда так как не знаю куда всунуть ) сделай рекомендации через теги как в
#  первом проекте в книги антонио миле python в примере


class StudyView(DetailView):
    """Обучение карточек"""
    template_name = 'lesson/study.html'
    context_object_name = 'lesson'
    model = Lesson

    def remove_duplicates(self):
        """Убираем слова, которые выучил пользователь"""
        lesson_obj = self.get_object()
        learned_words = LessonProgress.objects.get_or_create(user=self.request.user, lesson=lesson_obj)[0]
        if learned_words.cards.exists():  # если есть выученные слова
            all_words_in_lesson = lesson_obj.words.all()  # Получаем все слова из урока
            lesson_words = all_words_in_lesson.exclude(
                id__in=learned_words.cards.all())  # исключаем слова которые выучили
            return lesson_words
        return lesson_obj.words.all()  # если нету выученных слов отправляем все слова

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['words'] = self.remove_duplicates()
        return context

    def remembering_and_deleting_words_in_session(self):
        lesson_session = LessonSession(self.request)

        слово = Card.objects.get(id=1)

        if "Если пользователь знает слово то добавляем его в сессию":
            lesson_session.add(слово)
        elif "Если пользователь не знает слова и это слово находится в ссессии удаляем":
            lesson_session.remove(слово)

        if "Если это последнее слово тогда мы сохряняем сессию в базе прогресса":
            progress = LessonProgress.objects.get(user=self.request.user, lesson=self.get_object())
            for word_id in lesson_session.lesson:
                word = Card.objects.get(pk=word_id)
                progress.cards.add(word)
                # Todo:добавь код удаления ссесии
                # Todo:сделать редирект на страницу того что выучили или пршли все слова
        self.deleting_user_progress()

    def deleting_user_progress(self):
        progress = LessonProgress.objects.get(user=self.request.user, lesson=self.get_object())
        progress.cards.clear()  # очищаем выученные слова из модели прогресса пользователя
        # Todo:сделать редирек для перенаправления к началу обучения так как прогресс удален


class LessonDetailView(DetailView):
    """Просмотр урока"""
    model = Lesson
    template_name = 'lesson/detail.html'
    context_object_name = 'lesson'


class LessonCreateView(CreateView):
    """Создание урока"""
    model = Lesson
    form_class = LessonCreationForm
    template_name = 'lesson/create.html'

    def get_context_data(self, **kwargs):
        """Передаем в шаблон данные"""
        context = super().get_context_data(**kwargs)
        context['form_card'] = CardFormSet(queryset=Card.objects.none())  # queryset=Card.objects.none() в конструктор
        # CardFormSet, чтобы указать, что начальный набор данных должен быть пустым. Это означает, что при отображении
        # формы пользователю будут показаны пустые формы
        return context

    def form_valid(self, form):

        form_card = CardFormSet(data=self.request.POST)
        if form_card.is_valid():  # Проверка форм сетов (поля используемые несколько раз в одной форме)
            lesson = form.save(commit=False)
            lesson.course = get_object_or_404(Course, pk=self.kwargs['course_pk'])  # устанавливаем курс
            for card in form_card:
                card_instance = card.save()
                lesson.save()
                lesson.words.add(card_instance)  # Метод add является методом менеджера связанного поля и используется
                # для добавления объектов к связанному полю.
            return redirect(lesson.get_absolute_url())
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        context = self.get_context_data()
        context['form_lesson'] = form
        return self.render_to_response(context)


class LessonUpdateView(UpdateView):
    """Для редактирования уроков"""
    model = Lesson
    form_class = LessonCreationForm
    template_name = 'lesson/update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:  # данные, отправленные пользователем через форму, будут использоваться для создания или
            # обновления нескольких объектов Card, связанных с текущим объектом Lesson
            context['card_formset'] = CardFormSet(self.request.POST)
        else:  # получаем все слова, связанные с текущим объектом Lesson
            context['card_formset'] = CardFormSet(queryset=self.object.words.all())
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        card_formset = context['card_formset']

        if card_formset.is_valid():

            instances = card_formset.save(commit=False)
            for instance in instances:
                instance.save()
                self.object.words.add(instance)
            return super().form_valid(form)
        else:
            print(card_formset.errors)
            return self.render_to_response(self.get_context_data(form=form))
