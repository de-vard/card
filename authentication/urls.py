from django.urls import path

from authentication.viewsets.login import LoginView
from authentication.viewsets.refresh import RefreshViewSet
from authentication.viewsets.register import RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', RefreshViewSet.as_view(), name='refresh'),

]
