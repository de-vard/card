from django.contrib import admin
from course.models import Course
from lesson.models import Lesson


class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 0


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created', 'updated')  # Поля для отображения в списке
    search_fields = ('title', 'author__username')  # Поля для поиска
    list_filter = ('created', 'updated')  # Поля для фильтрации
    exclude = ('slug',)  # Исключаем поле slug из формы админки
    inlines = [LessonInline]

    def get_students(self, obj):
        # Возвращает список имен студентов, подписавшихся на курс
        return ", ".join([student.username for student in obj.students.all()])

    get_students.short_description = 'Студенты'  # Задаем заголовок для поля
