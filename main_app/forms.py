from django import forms
from django.forms import ModelForm
from .models import Category, Subcategory, Expense, Budget, Income, Goal


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class SubcategoryForm(ModelForm):
    class Meta:
        model = Subcategory
        fields = '__all__'


# Model for formatting date display on form:
class DateInput(forms.DateInput):
    input_type = 'date'

    def __init__(self, **kwargs):
        kwargs['format'] = '%d-%m-%Y'
        super().__init__(**kwargs)


class ExpenseForm(ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'subcategory', 'expense_date', 'expense_amount', 'description']

    # Function for implementing the calendar widget on form:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['expense_date'].widget = DateInput()


class BudgetForm(ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'budget_date', 'budget_amount']

    # Function for implementing the calendar widget on form:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['budget_date'].widget = DateInput()


class IncomeForm(ModelForm):
    class Meta:
        model = Income
        fields = ['income_date', 'income_amount', 'description']

    # Function for implementing the calendar widget on form:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['income_date'].widget = DateInput()


class GoalForm(ModelForm):
    class Meta:
        model = Goal
        fields = '__all__'

    # Function for implementing the calendar widget on form:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['goal_date'].widget = DateInput()
