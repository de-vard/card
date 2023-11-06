from django.contrib import messages
from django.shortcuts import redirect

from courses.models import CourseRegistration

from users.utils import create_action


def handle_subscription(request, course):
    """Поступление на курс"""
    user = request.user
    action = request.POST.get('action')
    if user and action:
        try:
            if action == 'follow':
                CourseRegistration.objects.select_related('course', 'user').get_or_create(course=course, user=user)
                create_action(user, 'поступил на курс', course)
            elif action == 'unfollow':
                CourseRegistration.objects.filter(course=course, user=user).delete()
            messages.add_message(request, messages.SUCCESS, f'Ты успешно {action}')
            return redirect(course.get_absolute_url())
        except course.DoesNotExist:
            messages.add_message(request, messages.SUCCESS, 'Упсс.. что-то пошло не так, сообщите нам об этом')


