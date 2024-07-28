from django.urls import path
from lesson import views


urlpatterns = [
    # Список курсов
    path('', views.LessonListAPIView.as_view(), name='lesson-list'),

    # Детальный просмотр курса
    path('<int:id>/', views.LessonRetrieveAPIView.as_view(), name='lesson-detail'),

    # Редактирование курса
    path('<int:id>/edit/', views.LessonRetrieveUpdateAPIView.as_view(), name='lesson-edit'),

    # Создание курса
    path('create/', views.LessonCreateAPIView.as_view(), name='lesson-create'),

    # Удаление курса
    path('<int:id>/delete/', views.LessonDestroyAPIView.as_view(), name='lesson-delete'),

    # Подписка на курс
    path('<int:pk>/learn/', views.LearnFlashcards.as_view(), name='lesson-learn'),

    # Отписка от курса
    path('<int:pk>/reset/result/', views.ResetResultLesson.as_view(), name='lesson-reset-result'),


]
