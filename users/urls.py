from django.urls import path
from users import views

app_name = 'users'

urlpatterns = [
    path('', views.UserListView.as_view(), name='list'),
    path('<slug:slug>/', views.UserDetailView.as_view(), name='detail'),

]
