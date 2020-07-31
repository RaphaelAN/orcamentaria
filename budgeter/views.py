from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse

from .forms import UserRegisterForm, TransactionCreationForm
from .models import Transaction, User, Budget


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


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
        user = self.request.user
        cutoff_date = user.get_budget_cutoff_date()
        return user.transaction_set.filter(date__range=[cutoff_date, timezone.now()]).order_by('-date')


@login_required()
def create_transaction(request):
    if request.method == 'POST':
        form = TransactionCreationForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse('home'))
    else:
        form = TransactionCreationForm()
    return render(request, 'budgeter/create_transaction.html')

