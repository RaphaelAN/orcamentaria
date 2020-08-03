from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse, reverse_lazy

from .forms import *
from .models import Transaction, User, Budget


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'{username} sua conta foi criada com sucesso')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


class UserUpdate(LoginRequiredMixin, generic.UpdateView):
    model = User
    fields = ['total_budget', 'budget_start_day']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('home')


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
        return user.transaction_set.all().order_by('-date')


@login_required()
def create_budget(request):
    if request.method == 'POST':
        form = BudgetCreationForm(request.POST, request=request)
        if form.is_valid():
            new_budget = form.save(commit=False)
            new_budget.user = request.user
            base_budget = request.user.get_base_budget()
            base_budget.allowed_spending -= new_budget.allowed_spending
            base_budget.save()
            new_budget.save()
            return redirect(reverse('home'))
    else:
        form = BudgetCreationForm()
    return render(request, 'budgeter/create_budget.html', {'form': form})


@login_required()
def create_transaction(request):
    if request.method == 'POST':
        form = TransactionCreationForm(request.POST, request=request)
        if form.is_valid():
            new_transaction = form.save(commit=False)
            new_transaction.user = request.user
            budget = form.cleaned_data['budget']
            new_transaction.budget = budget
            new_transaction.save()
            return redirect(reverse('home'))
    else:
        form = TransactionCreationForm(request=request)
    return render(request, 'budgeter/create_transaction.html', {'form': form})


class DeleteTransaction(LoginRequiredMixin, generic.DeleteView):
    model = Transaction
    success_url = reverse_lazy('transaction_history')


class DeleteBudget(LoginRequiredMixin, generic.DeleteView):
    model = Budget
    success_url = reverse_lazy('home')


class BudgetUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Budget
    fields = ['budget_name', 'allowed_spending', 'budget_color']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('home')


@login_required()
def transfer_budget(request):
    if request.method == 'POST':
        form = TransferBudgetForm(request.POST, request=request)
        if form.is_valid():
            value = form.cleaned_data['value']
            from_budget = form.cleaned_data['from_budget']
            to_budget = form.cleaned_data['to_budget']
            from_budget.allowed_spending -= value
            to_budget.allowed_spending += value
            from_budget.save()
            to_budget.save()
            return redirect(reverse_lazy('home'))
    else:
        form = TransferBudgetForm(request=request)

    return render(request, 'budgeter/transfer.html', {'form': form})


