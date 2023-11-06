from django.contrib import admin
from courses import models


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}  # автоматическое заполнение слага


@admin.register(models.Course)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(models.CourseRegistration)
class RegistrationAdmin(admin.ModelAdmin):
    pass
