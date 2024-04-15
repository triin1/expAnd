from django.db import models
from djmoney.models.fields import MoneyField


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"


class Subcategory(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "subcategories"


class Expense(models.Model):
    expense_date = models.DateField()
    expense_amount = MoneyField(max_digits=14, decimal_places=2, default_currency='AUD', default='0')
    budget_date = models.DateField()
    budget_amount = MoneyField(max_digits=14, decimal_places=2, default_currency='AUD', default='0')
    description = models.TextField(max_length=256, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.expense_amount} recorded on {self.date}"
