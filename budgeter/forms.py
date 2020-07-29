from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password', 'total_budget')


class UserBudgetUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('total_budget',)
