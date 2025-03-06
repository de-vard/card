import pytest
from fixtures.user import user, author
from fixtures.course import course

from lesson.models import Lesson


@pytest.mark.django_db
def test_create_lesson(user, author, course):
    lesson = Lesson.objects.create(title="Test lesson", course=course)
    assert lesson.title == "Test lesson"
    assert lesson.course == course
    assert lesson.course.author != user
    assert lesson.course.author == author
