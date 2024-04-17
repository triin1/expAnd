from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Sum, F
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Expense, Category, Subcategory, Budget, Income
from .forms import CategoryForm, SubcategoryForm, ExpenseForm, BudgetForm, IncomeForm


def home(request):
    return render(request, 'home.html')

# All category and subcategory related views:
def add_category(request):
    category_form = CategoryForm(request.POST)
    if category_form.is_valid():
        new_category = category_form.save(commit=False)
        new_category.save()
    return redirect('category_index')


def add_subcategory(request):
    subcategory_form = SubcategoryForm(request.POST)
    if subcategory_form.is_valid():
        new_subcategory = subcategory_form.save(commit=False)
        new_subcategory.save()
    return redirect('category_index')


def category_index(request):
    categories = Category.objects.all()
    category_form = CategoryForm()
    subcategory_form = SubcategoryForm()
    return render(request, 'categories/index.html', {
        'categories': categories,
        'category_form': category_form,
        'subcategory_form': subcategory_form,
    })


class CategoryUpdate(UpdateView):
    model = Category
    fields = '__all__'
    success_url = '/categories/'


class CategoryDelete(DeleteView):
    model = Category
    success_url = '/categories/'


class SubcategoryUpdate(UpdateView):
    model = Subcategory
    fields = '__all__'
    success_url = '/categories/'


class SubcategoryDelete(DeleteView):
    model = Subcategory
    success_url = '/categories/'


# All expenses related views:
def add_expense(request):
    expense_form = ExpenseForm(request.POST)
    if expense_form.is_valid():
        new_expense = expense_form.save(commit=False)
        new_expense.save()
    return redirect('expense_detail')


def expenses_index(request):
    expense_form = ExpenseForm()
    return render(request, 'expenses/index.html', {
        'expense_form': expense_form
    })


def expenses_detail(request):
    expenses = Expense.objects.all()
    return render(request, 'expenses/detail.html', {
        'expenses': expenses,
    })


class ExpenseUpdate(UpdateView):
    model = Expense
    fields = ['category', 'subcategory', 'expense_date', 'expense_amount', 'description']
    success_url = '/expenses/detail'


class ExpenseDelete(DeleteView):
    model = Expense
    success_url = '/expenses/detail'


def summary_index(request):
    expenses = Expense.objects.all()

    # Calculate total expenses by category and by month and order the expenses by month with most recent at the top:
    total_expenses = Expense.objects.annotate(month=TruncMonth('expense_date'), category_name=F('category__name')).order_by('-month').values('month', 'category_name').annotate(total_expenses=Sum('expense_amount'))
    
    return render(request, 'expenses/summary.html', {
        'expenses': expenses,
        'total_expenses': total_expenses
    })


# All budget related views:
def add_budget_amount(request):
    budget_form = BudgetForm(request.POST)
    if budget_form.is_valid():
        new_budget_amount = budget_form.save(commit=False)
        new_budget_amount.save()
    return redirect('budget_index')


def budget_index(request):
    budget = Budget.objects.all()
    budget_form = BudgetForm()

    # Defining the first day and the last day of the current month.
    first_day = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    first_day_next_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0) + timedelta(days=32)
    first_day_next_month = first_day_next_month.replace(day=1)
    last_day = first_day_next_month - timedelta(days=1)

    # Calculating the current month's budget amounts by category. The annotate defines calculation parameters of month and category name
    # and sums up the budget amounts based on these parameters. Filter uses first and last day of the month to filter out the sums by
    # category only for the current month.
    current_budget = Budget.objects.annotate(month=TruncMonth('budget_date'), category_name=F('category__name')).values('month', 'category_name').annotate(current_budget=Sum('budget_amount')).filter(budget_date__gte=first_day, budget_date__lte=last_day)

    return render(request, 'budget/index.html', {
        'budget_form': budget_form,
        'budget': budget,
        'current_budget': current_budget,
    })


class BudgetUpdate(UpdateView):
    model = Budget
    fields = '__all__'
    success_url = '/budget/'


class BudgetDelete(DeleteView):
    model = Budget
    success_url = '/budget/'


# All income related views:
# Page to add a form for new income to:
def new_income(request):
    income_form = IncomeForm()
    return render(request, 'income/new.html', {
        'income_form': income_form
    })


# New income form (added to the new_income page):
def add_income(request):
    income_form = IncomeForm(request.POST)
    if income_form.is_valid():
        new_income_amount = income_form.save(commit=False)
        new_income_amount.save()
    return redirect('income_index')


def income_index(request):
    income = Income.objects.all()

    return render(request, 'income/index.html', {
        'income': income,
    })