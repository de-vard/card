from rest_framework import serializers
from rest_framework.reverse import reverse

from course.models import Course, RegisteredUsers
from lesson.serializers import LessonSerializerList
from user.serializers import UserSerializer


class CourseSerializerBase(serializers.ModelSerializer):
    course_author = UserSerializer(source='author', read_only=True)
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    num_students = serializers.SerializerMethodField()
    num_lessons = serializers.SerializerMethodField()
    num_liked = serializers.SerializerMethodField()
    num_disliked = serializers.SerializerMethodField()
    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = (
            'title',
            'author',
            'num_liked',
            'num_disliked',
            'num_students',
            'num_lessons',
            'absolute_url',
        )

    def get_num_students(self, obj):
        return obj.students.count()

    def get_num_lessons(self, obj):
        return obj.lessons.count()

    def get_num_liked(self, obj):
        return RegisteredUsers.objects.filter(course=obj, liked=True).count()

    def get_num_disliked(self, obj):
        return RegisteredUsers.objects.filter(course=obj, disliked=True).count()

    def get_absolute_url(self, obj):
        return reverse('course-detail', args=[obj.pk])


class CourseSerializerList(CourseSerializerBase):
    class Meta(CourseSerializerBase.Meta):
        fields = CourseSerializerBase.Meta.fields + (
            'course_author',
        )


class CourseSerializerDetails(CourseSerializerBase):
    lessons = LessonSerializerList(many=True, read_only=True)

    class Meta(CourseSerializerBase.Meta):
        fields = CourseSerializerBase.Meta.fields + (
            'course_author',
            'lessons',
        )
