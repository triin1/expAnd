from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from .models import Expense, Category
from .forms import CategoryForm, SubcategoryForm


def home(request):
    return render(request, 'home.html')


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


class ExpenseCreate(CreateView):
    model = Expense
    fields = ['category', 'expense_date', 'expense_amount', 'description']
    # success_url = "/expenses/"
