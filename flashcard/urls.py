from django.urls import path
from flashcard import views

urlpatterns = [
    # Список карточек
    path('', views.FlashCardListAPIView.as_view(), name='flashcard-list'),

    # Детальный просмотр карточки
    path('<int:id>/', views.FlashCardRetrieveAPIView.as_view(), name='flashcard-detail'),

    # Редактирование карточки
    path('<int:id>/edit/', views.FlashCardRetrieveUpdateAPIView.as_view(), name='flashcard-edit'),

    # Создание карточки
    path('create/', views.FlashCardCreateAPIView.as_view(), name='flashcard-create'),

    # Удаление карточки
    path('<int:id>/delete/', views.FlashCardDestroyAPIView.as_view(), name='flashcard-delete'),

    # Отметить карточку как известную
    path('<int:pk>/know/', views.KnowFlashCard.as_view(), name='flashcard-know'),

    # Отметить карточку как неизвестную
    path('<int:pk>/unknown/', views.UnknownFlashCard.as_view(), name='flashcard-unknown'),
]
