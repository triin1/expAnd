from django.db import models
from djmoney.models.fields import MoneyField
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"
        ordering = ['name']


class Subcategory(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "subcategories"


class Expense(models.Model):
    expense_date = models.DateField()
    expense_amount = MoneyField(max_digits=14, decimal_places=2, default_currency='AUD')
    description = models.TextField(max_length=256, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.expense_amount} recorded on {self.expense_date}"


class Budget(models.Model):
    budget_date = models.DateField()
    budget_amount = MoneyField(max_digits=14, decimal_places=2, default_currency='AUD')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.budget_amount} recorded on {self.budget_date}"
    
    class Meta:
        verbose_name_plural = "budget"


class Income(models.Model):
    income_date = models.DateField()
    income_amount = MoneyField(max_digits=14, decimal_places=2, default_currency='AUD')
    description = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.income_amount} recorded on {self.income_date}"

    class Meta:
        verbose_name_plural = "income"


class Goal(models.Model):
    name = models.CharField(max_length=256)
    goal_amount = MoneyField(max_digits=14, decimal_places=2, default_currency='AUD')
    goal_date = models.DateField('Goal target date', null=True, blank=True)
    description = models.TextField(max_length=256, blank=True)
    amount_saved = MoneyField(max_digits=14, decimal_places=2, default_currency='AUD', default='0', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return f"Goal {self.name} of {self.goal_amount}"
