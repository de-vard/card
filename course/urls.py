from django.urls import path
from course import views


urlpatterns = [
    # Список курсов
    path('', views.CourseListAPIView.as_view(), name='course-list'),

    # Детальный просмотр курса
    path('<int:id>/', views.CourseRetrieveAPIView.as_view(), name='course-detail'),

    # Редактирование курса
    path('<int:id>/edit/', views.CourseRetrieveUpdateAPIView.as_view(), name='course-edit'),

    # Создание курса
    path('create/', views.CourseCreateAPIView.as_view(), name='course-create'),

    # Удаление курса
    path('<int:id>/delete/', views.CourseDestroyAPIView.as_view(), name='course-delete'),

    # Подписка на курс
    path('<int:pk>/enroll/', views.EnrollCourse.as_view(), name='course-enroll'),

    # Отписка от курса
    path('<int:pk>/unenroll/', views.UnenrollCourse.as_view(), name='course-unenroll'),

    # Лайк курса
    path('<int:pk>/like/', views.LikeCourse.as_view(), name='course-like'),

    # Дизлайк курса
    path('<int:pk>/dislike/', views.DislikeCourse.as_view(), name='course-dislike'),
]
