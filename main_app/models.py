from django.db import models
from djmoney.models.fields import MoneyField

class Expense(models.Model):
    category = models.CharField(max_length=50)
    subcategory = models.CharField(max_length=50)
    expense_date = models.DateField()
    expense_amount = MoneyField(max_digits=14, decimal_places=2, default_currency='AUD', default='0')
    budget_date = models.DateField()
    budget_amount = MoneyField(max_digits=14, decimal_places=2, default_currency='AUD', default='0')
    description = models.TextField(max_length=256, blank=True)

    def __str__(self):
        return f"{self.expense_amount} recorded in {self.category} and {self.subcategory} on {self.date}"
