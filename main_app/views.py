from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Sum
from django.db.models.functions import TruncMonth, TruncYear
# import datetime
from .models import Expense, Category, Subcategory
from .forms import CategoryForm, SubcategoryForm, ExpenseForm


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
    # total_expenses = Expense.objects.filter(expense_date__year=now.year, expense_date__month=now.month).aggregate(total_expenses=Sum('expense_amount'))['total_expenses']
    total_expenses = Expense.objects.annotate(month=TruncMonth('expense_date')).values('month').annotate(total_expenses=Sum('expense_amount'))
    return render(request, 'expenses/summary.html', {
        'expenses': expenses,
        # 'sum_expenses': sum_expenses,
        # 'year': now.year,
        # 'month': now.strftime('%B'),
        'total_expenses': total_expenses
    })

