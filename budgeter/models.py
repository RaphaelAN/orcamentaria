from django.db import models
from django.utils import timezone
from django.db.models import signals, Sum
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from colorfield.fields import ColorField
from decimal import Decimal
import datetime
from dateutil.relativedelta import relativedelta

# Base budget used to aggregate transactions without a user specified budget
BASE_BUDGET_NAME = "Outras Despesas"


class User(AbstractUser):
    BUDGET_START_DAY_OPTIONS = [(x, str(x)) for x in range(1, 29)]

    total_budget = models.DecimalField(decimal_places=2, max_digits=15, default=0, verbose_name='Orçamento Total')
    budget_start_day = models.IntegerField(choices=BUDGET_START_DAY_OPTIONS, default=1,
                                           verbose_name='Dia de inicio do orçamento')

    def get_base_budget(self):
        try:
            base_budget = self.budget_set.get(budget_name=BASE_BUDGET_NAME)
        except ObjectDoesNotExist:

            # budget created with allowed_spending zero to avoid recursion in get_allocated_budget
            base_budget = Budget.objects.create(user=self, budget_name=BASE_BUDGET_NAME,
                                                allowed_spending=0)
            allowed_spending = self.total_budget - self.get_allocated_budget()
            base_budget.allowed_spending = allowed_spending
            base_budget.save()

        return base_budget

    def get_allocated_budget(self):
        allocated_budget = self.budget_set.all().aggregate(Sum('allowed_spending'))['allowed_spending__sum']

        # exclude base budget allowed_spending as it's not allocated yet
        allocated_budget -= self.get_base_budget().allowed_spending
        return allocated_budget

    def get_spent_budget(self):
        spent_budget = self.transaction_set.all().aggregate(Sum('value'))['value__sum']

        if spent_budget is None:
            return Decimal('0.00')

        return spent_budget

    def get_spent_percentage(self):
        spent_budget = self.get_spent_budget()
        if spent_budget == 0 or self.total_budget == 0:
            return 0
        percentage = int((spent_budget/self.total_budget) * 100)
        if percentage > 100:
            return 100
        return percentage

    def get_budget_cutoff_date(self):
        today = timezone.now()
        cutoff_date = datetime.datetime(today.year, today.month, self.budget_start_day) - relativedelta(months=1)
        return cutoff_date

    def __str__(self):
        return self.username


class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    budget_name = models.CharField(max_length=200, verbose_name='Nome do Orçamento')
    allowed_spending = models.DecimalField(decimal_places=2, max_digits=15,verbose_name='Valor')
    spent = models.DecimalField(default=0, decimal_places=2, max_digits=15)
    budget_color = ColorField(default='#FF0000', verbose_name="Cor do Orçamento")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_spent_budget(self):
        spent_budget = self.transaction_set.all().aggregate(Sum('value'))['value__sum']

        if spent_budget is None:
            return Decimal('0.00')

        return spent_budget

    def get_spent_percentage(self):
        spent_budget = self.get_spent_budget()
        if spent_budget == 0 or self.allowed_spending == 0:
            return 0
        percentage = int((spent_budget/self.allowed_spending) * 100)
        if percentage > 100:
            return 100
        return percentage

    def __str__(self):
        return self.budget_name


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, verbose_name='Orçamento')
    title = models.CharField(max_length=200, verbose_name='Despesa')
    value = models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Valor')
    date = models.DateField(default=timezone.now, verbose_name='Data')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']


@receiver(signals.post_save, sender=User)
def update_base_budget(sender, instance, **kwargs):
    base_budget = instance.get_base_budget()
    base_budget.allowed_spending = instance.total_budget - instance.get_allocated_budget()
    base_budget.save()


@receiver(signals.post_save, sender=Budget)
def update_base_budget_from_budget(sender, instance, **kwargs):
    user = instance.user
    base_budget = user.get_base_budget()
    if instance == base_budget:
        return
    base_budget.allowed_spending = user.total_budget - user.get_allocated_budget()
    base_budget.save()


@receiver(signals.pre_delete, sender=Budget)
def point_transaction_to_base_budget(sender, instance, **kwargs):
    budget_transactions = instance.transaction_set.all()
    base_budget = instance.user.get_base_budget()
    base_budget.allowed_spending += instance.allowed_spending
    base_budget.save()
    for transaction in budget_transactions:
        transaction.budget = base_budget
        transaction.save()
