from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Transaction, User, Budget


def home(request):
    user = request.user
    user_spent_budget = user.get_spent_budget()
    context = {
        'user_spent_budget': user_spent_budget,
    }
    return render(request, 'budgeter/home.html', context)


class BudgetView(LoginRequiredMixin, generic.DetailView):
    model = Budget
    template_name = 'budgeter/budget.html'
