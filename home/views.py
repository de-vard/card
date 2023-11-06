from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from home.utils import get_actions
from users.models import Action


class DashboardListView(LoginRequiredMixin, ListView):
    model = Action
    context_object_name = 'actions'
    template_name = 'home/dashboard.html'
    login_url = 'account_login'  # перенаправляет если пользователь не авторизирован

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['actions'] = get_actions(self.request.user)  # вызываем функцию get_actions
        return context
