from django.contrib.auth.mixins import LoginRequiredMixin

from django.db.models import Count
from django.shortcuts import render

from django.views.generic import CreateView, DetailView, ListView

from courses.logical import handle_subscription
from courses.models import Course

from users.utils import create_action


class CourseListView(ListView):
    """Список курсов как своих так и всех"""
    model = Course
    context_object_name = 'all_courses'
    template_name = 'courses/list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.kwargs.get('owner'):
            queryset = queryset.filter(author=self.request.user)  # фильтрация по автору
        queryset = queryset.annotate(
            lesson_count=Count('lesson'),  # количество уроков
            user_count=Count('registrations')  # количество записанных пользователей на курс
        )
        sort = self.request.GET.get('sort')
        if sort:
            queryset = queryset.order_by(f'-{sort}')

        return queryset


class CourseDetailView(DetailView):
    """Детальный просмотр"""
    model = Course
    template_name = 'courses/detail.html'
    context_object_name = 'course'

    def post(self, request, *args, **kwargs):
        """Переопределил пост для обработки подписок"""
        course = self.get_object()
        handle_subscription(request, course)
        return self.get(request, *args, **kwargs)


class CourseCreateView(LoginRequiredMixin, CreateView):
    """ Класс для создания курса """
    model = Course
    fields = ['level', 'title']  # атрибут, последовательность имен полей модели, которые должны присутствовать в форме
    template_name = 'courses/create.html'
    login_url = 'account_login'  # перенаправляет если пользователь не авторизирован

    def form_valid(self, form):
        """ Метод автоматически устанавливает автора """
        form.instance.author = self.request.user
        response = super().form_valid(form)
        create_action(self.request.user, 'Создал курс', form.instance)  # form.instance - это атрибут формы,
        # который содержит экземпляр модели
        return response


def list_of_training_courses(request):
    """Функция выводит список курсов на которые подписан пользователь """
    users = request.user
    courses = users.registered_courses.all()
    context = {
        'courses': courses,
    }

    return render(request, 'users/learning.html', context=context)


