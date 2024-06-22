from django.contrib import admin
from course.models import Course, CourseRegistration


class CourseRegistrationInline(admin.TabularInline):
    model = CourseRegistration
    extra = 1
    readonly_fields = ('user', 'date')  # Поля, которые нельзя редактировать


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created', 'updated')  # Поля для отображения в списке
    search_fields = ('title', 'author__username')  # Поля для поиска
    list_filter = ('created', 'updated')  # Поля для фильтрации
    inlines = [CourseRegistrationInline]  # Инлайны для CourseRegistration
    exclude = ('slug',)  # Исключаем поле slug из формы админки


@admin.register(CourseRegistration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('course', 'user', 'date')  # Поля для отображения в списке
    search_fields = ('course__title', 'user__username')  # Поля для поиска
    list_filter = ('date',)  # Поля для фильтрации
