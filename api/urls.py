from django.urls import path, include
from rest_framework import routers

from .views import CourseViewSet, EnrollCourseView, UnenrollCourseView, LessonViewSet, FlashCardViewSet

router = routers.DefaultRouter()
router.register('courses',  CourseViewSet, basename='course')
router.register('lessons',  LessonViewSet, basename='lesson')
router.register('flashcard',  FlashCardViewSet, basename='flashcard')

urlpatterns = [
    path('', include(router.urls)),
    path('courses/<int:pk>/enroll/', EnrollCourseView.as_view(), name='enroll-course'),
    path('courses/<int:pk>/unenroll/', UnenrollCourseView.as_view(), name='unenroll-course'),
]
