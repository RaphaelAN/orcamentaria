from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm, ModelChoiceField, ValidationError, DateTimeField, SelectDateWidget
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

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_allowed_spending(self):
        unallocated_budget = self.request.user.get_base_budget().allowed_spending
        allowed_spending = self.cleaned_data.get('allowed_spending')
        if allowed_spending > unallocated_budget:
            raise ValidationError('Valor do novo orçamento excede seu orçamento mensal.')
        return allowed_spending


class TransactionCreationForm(ModelForm):
    budget = ModelChoiceField(label="Orçamento", queryset=None)
    date = DateTimeField(label='Data', widget=SelectDateWidget)

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if request:
            user = request.user
            self.fields['budget'].queryset = user.budget_set.all()

    class Meta:
        model = Transaction
        fields = ('title', 'value',)
