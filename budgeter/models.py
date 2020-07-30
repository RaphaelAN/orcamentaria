from django.db import models
from django.utils import timezone
from django.db.models import signals, Sum
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from decimal import Decimal

# Base budget used to aggregate transactions without a user specified budget
BASE_BUDGET_NAME = "Outros Gastos"


class User(AbstractUser):
    total_budget = models.DecimalField(decimal_places=2, max_digits=15, default=0)

    # TODO change save to signal
    """
    def save(self, *args, **kwargs):
        created = not self.pk
        super().save(*args, **kwargs)
        if created:
            Budget.objects.create(user=self, budget_name=BASE_BUDGET_NAME, allowed_spending=self.total_budget)
    """

    def get_base_budget(self):
        return self.budget_set.get(budget_name=BASE_BUDGET_NAME)

    def get_spent_budget(self):
        spent_budget = self.transaction_set.all().aggregate(Sum('value'))['value__sum']

        if spent_budget is None:
            return Decimal('0.00')

        return spent_budget

    def __str__(self):
        return self.username


class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    budget_name = models.CharField(max_length=200)
    allowed_spending = models.DecimalField(decimal_places=2, max_digits=15)
    spent = models.DecimalField(default=0, decimal_places=2, max_digits=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_spent_budget(self):
        spent_budget = self.transaction_set.all().aggregate(Sum('value'))['value__sum']

        if spent_budget is None:
            return Decimal('0.00')

        return spent_budget

    def __str__(self):
        return self.budget_name


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    value = models.DecimalField(decimal_places=2, max_digits=15)
    date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


@receiver(signals.post_save, sender=User)
def create_base_budget(sender, instance, **kwargs):
    Budget.objects.get_or_create(user=instance, budget_name=BASE_BUDGET_NAME, allowed_spending=instance.total_budget)


@receiver(signals.pre_delete, sender=Budget)
def point_transaction_to_base_budget(sender, instance, **kwargs):
    budget_transactions = instance.transaction_set.all()
    base_budget = instance.user.get_base_budget()
    for transaction in budget_transactions:
        transaction.budget = base_budget
        transaction.save()
