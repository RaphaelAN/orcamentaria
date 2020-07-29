from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import UserRegistrationForm, UserBudgetUpdateForm
from .models import User, Budget, Transaction


class CustomUserAdmin(UserAdmin):
    add_form = UserRegistrationForm
    form = UserBudgetUpdateForm
    model = User
    list_display = ['username', 'total_budget']


admin.site.register(User, UserAdmin)
admin.site.register(Transaction)
admin.site.register(Budget)

