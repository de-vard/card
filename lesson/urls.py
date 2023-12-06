from django.urls import path
from lesson import views

app_name = 'lesson'

urlpatterns = [

    path('study/<int:pk>/', views.StudyView.as_view(), name='study'),
    path('detail/<int:pk>/', views.LessonDetailView.as_view(), name='detail'),
    path('create/<int:course_pk>/', views.LessonCreateView.as_view(), name='create'),
    path('update/<int:pk>/', views.LessonUpdateView.as_view(), name='update'),




]
