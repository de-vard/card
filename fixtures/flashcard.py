import pytest
from fixtures.lesson import lesson
from fixtures.user import user
from flashcard.models import FlashCard

# Данные для создания флешкарточек
data_flashcards = [
    {
        "english_word": "apple",
        "russian_word": "яблоко",
        "transcription": "ˈæp.l̩",
        "image": None,
        "sound": None,
    },
    {
        "english_word": "banana",
        "russian_word": "банан",
        "transcription": "bəˈnæn.ə",
        "image": None,
        "sound": None,
    },
    {
        "english_word": "grape",
        "russian_word": "виноград",
        "transcription": "ɡreɪp",
        "image": None,
        "sound": None,
    }
]


@pytest.fixture
def flashcard1(db, lesson, user) -> FlashCard:
    flashcard = FlashCard.objects.create(lesson=lesson, **data_flashcards[0])
    flashcard.learner.add(user)
    return flashcard


@pytest.fixture
def flashcard2(db, lesson, user) -> FlashCard:
    flashcard = FlashCard.objects.create(lesson=lesson, **data_flashcards[1])
    flashcard.learner.add(user)
    return flashcard


@pytest.fixture
def flashcard3(db, lesson, user) -> FlashCard:
    flashcard = FlashCard.objects.create(lesson=lesson, **data_flashcards[2])
    flashcard.learner.add(user)
    return flashcard
