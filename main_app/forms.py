from django import forms
from django.forms import ModelForm
from .models import Category, Subcategory, Expense, Budget, Income, Goal


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }


class SubcategoryForm(ModelForm):
    class Meta:
        model = Subcategory
        fields = ['category', 'name']

        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }

    # Function for making category selection user specific:
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(user=user)


# Form for formatting date display on form. Do not flip the year-month-day display around, it will break the date showing up in the edit function:
class DateInput(forms.DateInput):
    input_type = 'date'

    def __init__(self, **kwargs):
        kwargs['format'] = '%Y-%m-%d'
        super().__init__(**kwargs)


class ExpenseForm(ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'subcategory', 'expense_date', 'expense_amount', 'description']

        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'subcategory': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'style': 'height: 80px;'}),
        }

    # Function for making category and subcategory selections user specific and implementing the calendar widget on form:
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(user=user)
        self.fields['subcategory'].queryset = Subcategory.objects.filter(user=user)
        self.fields['expense_date'].widget = DateInput()


class BudgetForm(ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'budget_date', 'budget_amount']

        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
        }

    # Function for making category selections user specific and implementing the calendar widget on form:
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(user=user)
        self.fields['budget_date'].widget = DateInput()


class IncomeForm(ModelForm):
    class Meta:
        model = Income
        fields = ['income_date', 'income_amount', 'description']

        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }

    # Function for implementing the calendar widget on form:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['income_date'].widget = DateInput()


class GoalForm(ModelForm):
    class Meta:
        model = Goal
        fields = ['name', 'goal_amount', 'goal_date', 'description', 'amount_saved']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'style': 'height: 80px;'}),
        }

    # Function for implementing the calendar widget on form:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['goal_date'].widget = DateInput()
