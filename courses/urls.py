from django.urls import path
from courses import views

app_name = 'course'

urlpatterns = [
    path('', views.CourseListView.as_view(), name='list'),
    path('new/', views.CourseCreateView.as_view(), name='create'),
    path('learning/', views.list_of_training_courses,  name='learning'),
    path('author/<str:owner>/', views.CourseListView.as_view(), name='owner_list'),
    path('<slug:slug>/', views.CourseDetailView.as_view(), name='detail'),

]
