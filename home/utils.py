from users.models import Action


def get_actions(user):
    """Получаем действия пользователей"""
    actions = Action.objects.exclude(user=user).prefetch_related('user')  # все действия пользователей
    following_ids = user.following.values_list('id',
                                               flat=True)  # список пользователей, на которых подписан пользователь
    if following_ids:  # Если пользователь подписан на других, то извлекаем только их действия
        actions = actions.filter(user_id__in=following_ids)  # фильтруем QuerySet actions, чтобы оставить только те
        # действия, у которых поле user_id содержится в списке following_ids
        actions = actions[:10]
    return actions
