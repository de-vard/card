from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe

from .models import CustomUser, Follow


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'date_of_birth', 'get_photo', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'date_of_birth')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    readonly_fields = ('get_photo', 'date_joined', 'last_login')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info',
         {'fields': ('first_name', 'last_name', 'email', 'date_of_birth', 'photo', 'get_photo', 'slug')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'date_of_birth', 'photo')}
         ),
    )

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50" height="60" />')
        return 'Фото отсутствует'

    get_photo.short_description = 'Фото'


admin.site.register(CustomUser, CustomUserAdmin)


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user_from', 'user_to', 'created')
    search_fields = ('user_from__username', 'user_to__username')
    list_filter = ('created',)
    date_hierarchy = 'created'


admin.site.register(Follow, FollowAdmin)
