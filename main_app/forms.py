from django import forms
from django.forms import ModelForm
from .models import Category, Subcategory, Expense


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class SubcategoryForm(ModelForm):
    class Meta:
        model = Subcategory
        fields = '__all__'


# model for formatting date display on form:
class DateInput(forms.DateInput):
    input_type = 'date'

    def __init__(self, **kwargs):
        kwargs['format'] = '%Y-%m-%d'
        super().__init__(**kwargs)


class ExpenseForm(ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'subcategory', 'expense_date', 'expense_amount', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['expense_date'].widget = DateInput()

