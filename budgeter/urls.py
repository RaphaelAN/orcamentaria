from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('config/<int:pk>/', views.UserUpdate.as_view(), name='user_update'),
    path('budget/', views.create_budget, name='create_budget'),
    path('budget/update/<int:pk>/', views.BudgetUpdate.as_view(), name='budget_update'),
    path('<int:pk>/', views.BudgetView.as_view(), name='budget'),
    path('transactions/', views.TransactionHistoryView.as_view(), name='transaction_history'),
    path('transaction/', views.create_transaction, name='create_transaction'),
    path('transaction/delete/<int:pk>/', views.DeleteTransaction.as_view(), name='delete_transaction'),
    path('budget/delete/<int:pk>/', views.DeleteBudget.as_view(), name='delete_budget'),
    path('transfer', views.transfer_budget, name='transfer_budget')
]
