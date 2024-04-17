from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Sum, F
from django.db.models.functions import TruncMonth
import datetime
from .models import Expense, Category, Subcategory
from .forms import CategoryForm, SubcategoryForm, ExpenseForm, BudgetForm


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
    # sum_expenses = Expense.objects.aggregate(Sum('expense_amount'))['expense_amount__sum']
    # now = datetime.datetime.now()
    # current_total = Expense.objects.filter(expense_date__year=now.year, expense_date__month=now.month).aggregate(total_expenses=Sum('expense_amount'))['total_expenses']
    # Calculate total expenses by category and by month and order the expenses by month with most recent at the top:
    total_expenses = Expense.objects.annotate(month=TruncMonth('expense_date'), category_name=F('category__name')).order_by('-month').values('month', 'category_name').annotate(total_expenses=Sum('expense_amount'))
    return render(request, 'expenses/summary.html', {
        'expenses': expenses,
        # 'sum_expenses': sum_expenses,
        # 'current_total': current_total,
        # 'year': now.year,
        # 'month': now.strftime('%B'),
        'total_expenses': total_expenses
    })


# All budget related views:
def budget_index(request):
    budget_form = BudgetForm()
    categories = Category.objects.all()
    return render(request, 'budget/index.html', {
        'categories': categories,
        'budget_form': budget_form,
    })


def add_budget_amount(request):
    budget_form = BudgetForm(request.POST)
    if budget_form.is_valid():
        new_budget_amount = budget_form.save(commit=False)
        new_budget_amount.save()
    return redirect('budget_index')
