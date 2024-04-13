from django.shortcuts import render
from django.views.generic.edit import CreateView
# from .models import Expense


def home(request):
    return render(request, 'home.html')

# class ExpenseCreate(CreateView):
#     model = Expense
#     fields = '__all__'
