from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm, ModelChoiceField

from .models import User, Transaction, Budget


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'total_budget', 'budget_start_day')


class UserBudgetUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('total_budget',)


class BudgetCreationForm(ModelForm):
    class Meta:
        model = Budget
        fields = ('budget_name', 'allowed_spending')


class TransactionCreationForm(ModelForm):
    budget = ModelChoiceField(label="Orçamento", queryset=None)

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if request:
            user = request.user
            self.fields['budget'].queryset = user.budget_set.all()

    class Meta:
        model = Transaction
        fields = ('title', 'value', 'date')
