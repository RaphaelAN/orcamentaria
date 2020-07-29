from django.urls import path
from . import views
from .views import home
urlpatterns = [
    path('', views.home, name='home'),
    path('<int:pk>/', views.BudgetView.as_view(), name='budget')
]
