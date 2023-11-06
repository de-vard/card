from django.shortcuts import  render
from django.views.generic import DetailView, ListView
from django.contrib.auth import get_user_model

from users.utils import handle_subscription


class UserDetailView(DetailView):
    """Детальны просмотр пользователя"""
    model = get_user_model()
    template_name = 'users/detail.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['is_registered'] = self.object.following.filter(id=self.request.user.id).exists()
        return context

    def post(self, request, *args, **kwargs):
        """Переопределил пост для обработки подписок"""
        user_to = self.get_object()  # Пользователь на которого подписываются
        handle_subscription(request, user_to)
        return self.get(request, *args, **kwargs)


class UserListView(ListView):
    """Список пользователей"""
    model = get_user_model()
    template_name = 'users/list.html'
    context_object_name = 'object_user'



