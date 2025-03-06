import pytest
from fixtures.user import author

from course.models import Course


@pytest.fixture
def course(author):
    return Course.objects.create(author=author, title="Test title course")
