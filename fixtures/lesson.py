import pytest
from fixtures.course import course

from lesson.models import Lesson


@pytest.fixture
def lesson(course):
    return Lesson.objects.create(title="Test lesson", course=course)
