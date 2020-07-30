from decimal import Decimal

from django.test import TestCase
from .models import User, Transaction, Budget


class UserModelTests(TestCase):

    def setUp(self):
        user = User(username="user", total_budget=100)
        user.save()
        t1 = Transaction(user=user, budget=user.get_base_budget(), value=10)
        t2 = Transaction(user=user, budget=user.get_base_budget(), value=15)
        t3 = Transaction(user=user, budget=user.get_base_budget(), value=20)
        t1.save()
        t2.save()
        t3.save()

    def test_User_get_spent_budget(self):
        """
        Tests the sum of a user transactions given by User.get_spent_budget method
        """
        user = User.objects.get(id=1)

        self.assertAlmostEqual(user.get_spent_budget(), Decimal('45'))

    def test_Budget_get_spent_budget(self):
        """
        Tests the sum of a budget's transactions given by  Budget.get_spent_budget method
        """
        budget = Budget.objects.get(id=1)
        self.assertAlmostEqual(budget.get_spent_budget(), Decimal('45'))

