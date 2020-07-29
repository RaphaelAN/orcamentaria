from decimal import Decimal

from django.test import TestCase
from .models import User, Transaction, Budget


class UserModelTests(TestCase):

    def test_sum_of_user_transactions(self):
        """
        Tests the sum of transactions given by get_spent_budget function
        """
        user = User(user_name="user", total_budget=100)
        user.save()
        t1 = Transaction(user=user, budget=user.get_base_budget(), value=10)
        t2 = Transaction(user=user, budget=user.get_base_budget(), value=15)
        t3 = Transaction(user=user, budget=user.get_base_budget(), value=20)
        t1.save()
        t2.save()
        t3.save()
        sum = 45
        self.assertIs(user.get_spent_budget(), sum)
