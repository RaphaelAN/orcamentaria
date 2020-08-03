from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm, ModelChoiceField, ValidationError, DateField, SelectDateWidget, Form
from django import forms
from datetime import date
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
            raise ValidationError('Valor do orçamento excede seu orçamento mensal.')
        return allowed_spending


class TransactionCreationForm(ModelForm):
    budget = ModelChoiceField(label="Orçamento", queryset=None)
    date = DateField(label='Data', initial=date.today(), widget=SelectDateWidget)

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if request:
            user = request.user
            self.fields['budget'].queryset = user.budget_set.all()

    class Meta:
        model = Transaction
        fields = ('title', 'value', 'date')


class TransferBudgetForm(Form):
    from_budget = ModelChoiceField(label='De', queryset=None)
    to_budget = ModelChoiceField(label='Para', queryset=None)
    value = forms.DecimalField(label='Valor')

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if request:
            user = request.user
            self.fields['from_budget'].queryset = user.budget_set.all()
            self.fields['to_budget'].queryset = user.budget_set.all()

    def clean_value(self):
        from_budget = self.cleaned_data.get('from_budget')
        value = self.cleaned_data.get('value')

        if value > from_budget.allowed_spending:
            raise ValidationError('Valor maior que o disponivel para transferencia!')
        return value
