import pytest
from fixtures.user import author, user

from course.models import Course


@pytest.mark.django_db
def test_create_post(author, user):
    course = Course.objects.create(author=author, title="Test title course")
    assert course.title == "Test title course"
    assert course.author == author
    assert course.author != user
