from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = get_user_model()
        fields = ('email', 'username', 'last_name', 'is_staff', 'is_active')

    class Media:
        css = {
            'all': 'form.css',
        }


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = get_user_model()
        fields = ('email', 'username', 'last_name', 'is_staff', 'is_active')
