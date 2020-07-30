from django.urls import path
from . import views
from .views import home
urlpatterns = [
    path('', views.home, name='home'),
    path('<int:pk>/', views.BudgetView.as_view(), name='budget'),
    path('transactions/', views.TransactionHistoryView.as_view(), name='transaction_history'),
]
