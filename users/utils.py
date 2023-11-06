import datetime

from django.shortcuts import redirect
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from .models import Action, Contact
from django.contrib import messages


def create_action(user, verb, target=None):
    # user это пользователь, verb это строка описывающая действие, target это объект любой модели Django
    """Добавляет действия в модель активности"""
    now = timezone.now()  # берется текущее время
    last_minute = now - datetime.timedelta(seconds=60)  # отнимаем минуту
    similar_actions = Action.objects.filter(  # пытаемся получить такие же действий
        user_id=user.id,
        verb=verb,
        created__gte=last_minute  # __gte - это сокращение от “greater than or equal to” (больше или равно)
    )
    if target:
        target_ct = ContentType.objects.get_for_model(target)  # вы передаете экземпляр модели в метод get_for_model,
        # он возвращает вам экземпляр ContentType, который представляет эту модель
        similar_actions = similar_actions.filter(
            target_ct=target_ct,
            target_id=target.id
        )
    if not similar_actions:  # Если список similar_actions не пуст, то это означает, что уже есть похожие действия в
        # базе данных и код внутри блока if не будет выполнен.
        action = Action(user=user, verb=verb, target=target)
        action.save()
        return True
    return False


def handle_subscription(request, subscribed_object):
    """Подписка на пользователя"""
    user = request.user  # Пользователь, который подписывается
    action = request.POST.get('action')
    if user and action:
        try:
            if user == subscribed_object:  # если пользователь пытается подписаться на себя
                print('Кто-то пытается подписаться на самого себя')
            elif action == 'follow':  # user_from подписывается на user_to
                Contact.objects.get_or_create(user_from=user, user_to=subscribed_object)
                create_action(user, 'подписался', subscribed_object)
            elif action == 'unfollow':  # отписывается от него
                Contact.objects.filter(user_from=user, user_to=subscribed_object).delete()
            messages.add_message(request, messages.SUCCESS, f'Ты успешно {action}')
            return redirect(user.get_absolute_url())
        except subscribed_object.DoesNotExist:
            messages.add_message(request, messages.SUCCESS, 'Упсс.. что-то пошло не так, сообщите нам об этом')
