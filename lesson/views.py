from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, ListView

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
        lesson_obj_all = lesson_obj.words.all()  # если нету выученных слов отправляем все слова

        return lesson_obj_all

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['words'] = self.remove_duplicates()
        context['lesson'] = self.get_object()
        return context

    def post(self, request, *args, **kwargs):
        self.deleting_user_progress()  # выставляем первы для проверки удаляет ли пользователь результат или нет

        if not self.remove_duplicates():  # вызываем функцию проверки сколько слов осталось не изученно, и если не одно перенаправляем пользователя на страницу
            return self.result_about_learning_lesson()

        self.update_knowledge()  # вызывает функцию для работы с сохранением в сесси слов

        return super().get(request, *args, **kwargs)

    def update_knowledge(self):
        """Функция определяет знает пользователь слово или нет и сохраняет результат в сессию"""
        word_id = self.request.POST.get('word_id', None)  # значение слова
        knowledge = self.request.POST.get('knowledge', None)  # значение параметра знает человек слово или нет
        session = LessonSession(self.request)
        if knowledge == "known":
            session.add(word_id)
        elif knowledge == "unknown" and word_id in session.lesson:
            session.remove(word_id)

        last_or_not_last = self.request.POST.get('last', None)
        if last_or_not_last:  # слово пришло с отметкой что оно последнне, вызываем функцию сохранения сесси в БД
            self.save_session(
                session)  # передаем в функцию список выученных слов  сохранения сессии в прогрессе пользователя

    def save_session(self, session):
        """Берем слова из сессии и сохраняем их в модели прогресса пользователя"""
        words_in_session = session.lesson.copy()  # копируем список из сессии так как удаление слов из сессии присходи быстрее добавления ее в модель прогресса пользователя
        progress = LessonProgress.objects.get(user=self.request.user, lesson=self.get_object())
        for word_id in words_in_session:
            word = Card.objects.get(pk=word_id)
            progress.cards.add(word)

            session.remove(word)

    def deleting_user_progress(self):
        progress = LessonProgress.objects.get(user=self.request.user, lesson=self.get_object())
        lesson_del = self.request.POST.get('lesson_del', None)
        if lesson_del:
            progress.delete()

    def result_about_learning_lesson(self):
        """Код отрабатывается только после того как пользователь выучмл все слова из урока"""
        lesson = self.get_object()
        if self.remove_duplicates():  # проверям выучил ли пользователь все слова, если слова есть то пользователь изучил не все
            return redirect('lesson:study', pk=lesson.pk)

        context = {
            'lesson': lesson,
            'count_words': len(lesson.words.all())
        }
        return render(self.request, 'lesson/study_completion_info.html', context=context)


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
