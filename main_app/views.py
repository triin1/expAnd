from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from .models import Expense, Category
from .forms import SubcategoryForm


def home(request):
    return render(request, 'home.html')


class CategoryCreate(CreateView):
    model = Category
    fields = '__all__'
    success_url = "/categories/"


def add_subcategory(request):
    subcategory_form = SubcategoryForm(request.POST)
    if subcategory_form.is_valid():
        new_subcategory = subcategory_form.save(commit=False)
        new_subcategory.save()
    return redirect('category_index')


def category_index(request):
    categories = Category.objects.all()
    subcategory_form = SubcategoryForm()
    return render(request, 'categories/index.html', {
        'categories': categories,
        'subcategory_form': subcategory_form,
    })


class ExpenseCreate(CreateView):
    model = Expense
    fields = ['category', 'expense_date', 'expense_amount', 'description']
