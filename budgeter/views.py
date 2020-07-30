from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import Transaction, User, Budget


@login_required
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


class TransactionHistoryView(LoginRequiredMixin, generic.ListView):
    template_name = 'budgeter/transaction_history.html'
    context_object_name = 'transaction_history'

    def get_queryset(self):
        return self.request.user.transaction_set.all()
