from rest_framework import status

# Импортируем фикстуры для пользователя, автора и курса
from fixtures.user import user, author
from fixtures.course import course
from fixtures.lesson import lesson
from fixtures.flashcard import flashcard1, flashcard2, flashcard3
from flashcard.models import LearnerFlashCard


class TestFlashCard:
    endpoint = '/api/v1/flashcards/'

    def test_list(self, client, user):
        """Тест на получение списка карточек авторизованным пользователем"""
        # Авторизуем пользователя
        client.force_authenticate(user=user)

        # Отправляем GET-запрос на список карточек
        response = client.get(self.endpoint)

        # Проверяем, что ответ успешный (200 OK)
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve(self, client, user, flashcard1):
        """Тест на получение детальной информации о флешкарточке авторизованным пользователем"""

        # Авторизуем пользователя
        client.force_authenticate(user=user)

        # Отправляем GET-запрос на получение подробной информации о конкретном курсе
        response = client.get(self.endpoint + str(flashcard1.id) + "/")

        # Проверяем, что ответ успешный (200 OK)
        assert response.status_code == status.HTTP_200_OK

        # Проверяем, что идентификатор карточки совпадает с ожидаемым
        assert str(response.data['id']) == str(flashcard1.id)

        # Проверяем, что данные карточки корректные
        assert response.data['english_word'] == flashcard1.english_word
        assert response.data['russian_word'] == flashcard1.russian_word
        assert response.data['transcription'] == flashcard1.transcription

        # Проверяем, что карточка принадлежит правильному уроку
        assert response.data['lesson'] == flashcard1.lesson.id

    def test_create(self, client, author, lesson):
        """Тест на создание флешкарточки"""

        client.force_authenticate(user=author)

        data = {
            "english_word": "Apple",
            "russian_word": "Яблоко",
            "transcription": "[ˈæpl]",
            "lesson": lesson.id
        }
        response = client.post(self.endpoint + "create/", data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["english_word"] == data["english_word"]
        assert response.data["russian_word"] == data["russian_word"]
        assert response.data["transcription"] == data["transcription"]
        assert response.data["lesson"] == lesson.id

    def test_create_not_author(self, client, user, lesson):
        """Тест на создание карточки не пользователем"""
        client.force_authenticate(user=user)
        data = {
            "english_word": "Apple",
            "russian_word": "Яблоко",
            "transcription": "[ˈæpl]",
            "lesson": lesson.id
        }
        response = client.post(self.endpoint + "create/", data)
        # Ожидаем ошибку 403
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_edit(self, client, author, lesson, flashcard1):
        """Тест на редактирование карточку"""
        client.force_authenticate(user=author)
        data = {
            "english_word": "Apple",
            "russian_word": "Яблоко",
            "transcription": "[ˈæpl]",
            "lesson": lesson.id
        }
        response = client.put(self.endpoint + str(flashcard1.id) + "/edit/", data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['english_word'] == data['english_word']
        assert response.data['russian_word'] == data['russian_word']
        assert response.data['transcription'] == data['transcription']
        assert response.data['lesson'] == data['lesson']

    def test_edit_not_author(self, client, user, lesson, flashcard1):
        """Тест на редактирование карточку если он не автор """
        client.force_authenticate(user=user)
        data = {
            "english_word": "Apple",
            "russian_word": "Яблоко",
            "transcription": "[ˈæpl]",
            "lesson": lesson.id
        }
        response = client.put(self.endpoint + str(flashcard1.id) + "/edit/", data)
        # Ожидаем ошибку 403
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete(self, client, author, flashcard1):
        """Тест на удаление карточки"""
        client.force_authenticate(user=author)
        response = client.delete(self.endpoint + str(flashcard1.id) + "/delete/")
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_not_author(self, client, user, flashcard1):
        """Тест: пользователь, не являющийся автором, НЕ должен удалять карточку"""
        client.force_authenticate(user=user)
        response = client.delete(self.endpoint + str(flashcard1.id) + "/delete/")
        # Проверяем, что удаление запрещено (403 Forbidden)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_mark_known(self, client, user, flashcard1, course):
        """Тест на отметку карточки как известной"""
        client.force_authenticate(user=user)

        course.students.add(user)  # Сначала подписываем пользователя на курс
        response = client.post(self.endpoint + str(flashcard1.id) + "/know/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'marked as known'

        # Проверяем, что в БД есть запись и флаг `learned_word` == True
        learner_flashcard = LearnerFlashCard.objects.get(user=user, flashcard=flashcard1)
        assert learner_flashcard.learned_word is True

    def test_mark_known_if_user_not_enrolled(self, client, user, flashcard1):
        """Тест на проверку, что у не подписанного пользователя нет возможности отправлять запросы"""
        client.force_authenticate(user=user)
        response = client.post(self.endpoint + str(flashcard1.id) + "/know/")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_mark_unknown(self, client, user, flashcard1, course):
        """Тест на отметку карточки как неизвестной"""
        client.force_authenticate(user=user)
        course.students.add(user)  # Сначала подписываем пользователя на курс
        response = client.post(self.endpoint + str(flashcard1.id) + "/unknown/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'marked as unknown'

        # Проверяем, что в БД есть запись и флаг `learned_word` == False
        learner_flashcard = LearnerFlashCard.objects.get(user=user, flashcard=flashcard1)
        assert learner_flashcard.learned_word is False

    def test_mark_unknown_if_user_not_enrolled(self, client, user, flashcard1):
        """Тест на проверку, что у не подписанного пользователя нет возможности отправлять запросы"""
        client.force_authenticate(user=user)
        response = client.post(self.endpoint + str(flashcard1.id) + "/unknown/")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_mark_known_unauthenticated(self, client, flashcard1):
        """Тест: неавторизованный пользователь не может отметить карточку"""
        response = client.post(self.endpoint + str(flashcard1.id) + "/know/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED # Доступ запрещен без авторизации

    def test_mark_unknown_unauthenticated(self, client, flashcard1):
        """Тест: неавторизованный пользователь не может отметить карточку как неизвестную"""
        response = client.post(self.endpoint + str(flashcard1.id) + "/unknown/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_anonymous(self, client):
        """Тест на получение списка уроков неавторизованным пользователем"""
        response = client.get(self.endpoint)

        # Проверяем, что ответ содержит ошибку 401
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_anonymous(self, client, flashcard1):
        """Тест на получение детальной информации об уроке неавторизованным пользователем"""
        response = client.get(self.endpoint + str(flashcard1.id) + "/")

        # Проверяем, что ответ содержит ошибку 401
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_anonymous(self, client, author, lesson):
        """Тест на создание урока неавторизованным пользователем"""
        data = {
            "english_word": "Apple",
            "russian_word": "Яблоко",
            "transcription": "[ˈæpl]",
            "lesson": lesson.id
        }
        response = client.post(self.endpoint + 'create/', data)

        # Проверяем, что ответ содержит ошибку 401
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_edit_anonymous(self, client, lesson):
        """Тест на редактирование урока неавторизованным пользователем"""
        data = {
            "english_word": "Apple",
            "russian_word": "Яблоко",
            "transcription": "[ˈæpl]",
            "lesson": lesson.id
        }
        response = client.put(self.endpoint + str(lesson.id) + "/edit/", data)

        # Проверяем, что ответ содержит ошибку 401
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_anonymous(self, client, flashcard1):
        """Тест на удаление урока неавторизованным пользователем"""
        response = client.delete(self.endpoint + str(flashcard1.id) + "/delete/")

        # Проверяем, что ответ содержит ошибку 401
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
