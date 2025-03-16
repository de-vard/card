import pytest
from fixtures.user import user, author
from fixtures.course import course
from fixtures.lesson import lesson

from flashcard.models import FlashCard


@pytest.mark.django_db
def test_create_flashcard(user, author, course, lesson):
    flashcard = FlashCard.objects.create(
        english_word="book",
        russian_word="книга",
        transcription="book",
        lesson=lesson,
    )
    # Поле learner является ManyToManyField, поэтому его нельзя передавать в create().
    # Вместо этого пользователя добавляем отдельно через .set().
    flashcard.learner.set([user])

    # Проверяем, что пользователь действительно добавлен в список изучающих карточку
    assert user in flashcard.learner.all()

    assert flashcard.english_word == "book"
    assert flashcard.russian_word == "книга"
    assert flashcard.transcription == "book"
    assert flashcard.lesson == lesson
    assert flashcard.lesson.course.author != user
    assert flashcard.lesson.course.author == author
