from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Sum, F
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Expense, Category, Subcategory, Budget, Income, Goal
from .forms import CategoryForm, SubcategoryForm, ExpenseForm, BudgetForm, IncomeForm, GoalForm


# All general and authentication related views:
def home(request):
    return render(request, 'home.html')


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid sign up - please try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


# All category and subcategory related views:
@login_required
def add_category(request):
    category_form = CategoryForm(request.POST)
    if category_form.is_valid():
        new_category = category_form.save(commit=False)
        new_category.user = request.user
        new_category.save()
    return redirect('category_index')

@login_required
def add_subcategory(request):
    subcategory_form = SubcategoryForm(request.user, request.POST)
    if subcategory_form.is_valid():
        new_subcategory = subcategory_form.save(commit=False)
        new_subcategory.user = request.user
        # subcategory_form.instance.user = request.user
        new_subcategory.save()
    return redirect('category_index')


@login_required
def category_index(request):
    categories = Category.objects.filter(user=request.user)
    category_form = CategoryForm()
    subcategory_form = SubcategoryForm(user=request.user)
    return render(request, 'categories/index.html', {
        'categories': categories,
        'category_form': category_form,
        'subcategory_form': subcategory_form,
    })


class CategoryUpdate(LoginRequiredMixin, UpdateView):
    model = Category
    fields = ['name']
    success_url = '/categories/'


class CategoryDelete(LoginRequiredMixin, DeleteView):
    model = Category
    success_url = '/categories/'


class SubcategoryUpdate(LoginRequiredMixin, UpdateView):
    model = Subcategory
    fields = ['category', 'name']
    success_url = '/categories/'


class SubcategoryDelete(LoginRequiredMixin, DeleteView):
    model = Subcategory
    success_url = '/categories/'


# All expenses related views:
@login_required
# Page to add a form for new expense to:
def expenses_new(request):
    expense_form = ExpenseForm(user=request.user)
    return render(request, 'expenses/new.html', {
        'expense_form': expense_form
    })


@login_required
def add_expense(request):
    expense_form = ExpenseForm(request.user, request.POST)
    if expense_form.is_valid():
        new_expense = expense_form.save(commit=False)
        new_expense.user = request.user
        # expense_form.instance.user = request.user
        new_expense.save()
    return redirect('expense_detail')


@login_required
def expenses_detail(request):
    expenses = Expense.objects.filter(user=request.user)
    return render(request, 'expenses/detail.html', {
        'expenses': expenses,
    })


class ExpenseUpdate(LoginRequiredMixin, UpdateView):
    model = Expense
    fields = ['category', 'subcategory', 'expense_date', 'expense_amount', 'description']
    success_url = '/expenses/detail'


class ExpenseDelete(LoginRequiredMixin, DeleteView):
    model = Expense
    success_url = '/expenses/detail'


@login_required
def summary_index(request):
    expenses = Expense.objects.filter(user=request.user)

    # Calculate total expenses by category and by month and order the expenses by month with most recent at the top:
    total_expenses = Expense.objects.filter(user=request.user).annotate(month=TruncMonth('expense_date'), category_name=F('category__name')).order_by('-month').values('month', 'category_name').annotate(total_expenses=Sum('expense_amount'))
    
    return render(request, 'expenses/summary.html', {
        'expenses': expenses,
        'total_expenses': total_expenses
    })


# All budget related views:
@login_required
def add_budget_amount(request):
    budget_form = BudgetForm(request.user, request.POST)
    if budget_form.is_valid():
        new_budget_amount = budget_form.save(commit=False)
        new_budget_amount.user = request.user
        # budget_form.instance.user = request.user
        new_budget_amount.save()
    return redirect('budget_index')


@login_required
def budget_index(request):
    budget = Budget.objects.filter(user=request.user)
    budget_form = BudgetForm(user=request.user)

    # Defining the first day and the last day of the current month.
    first_day = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    first_day_next_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0) + timedelta(days=32)
    first_day_next_month = first_day_next_month.replace(day=1)
    last_day = first_day_next_month - timedelta(days=1)

    # Calculating the current month's budget amounts by category. The annotate defines calculation parameters of month and category name
    # and sums up the budget amounts based on these parameters. Filter uses first and last day of the month to filter out the sums by
    # category only for the current month.
    current_budget = Budget.objects.filter(user=request.user).annotate(month=TruncMonth('budget_date'), category_name=F('category__name')).values('month', 'category_name').annotate(current_budget=Sum('budget_amount')).filter(budget_date__gte=first_day, budget_date__lte=last_day)

    return render(request, 'budget/index.html', {
        'budget_form': budget_form,
        'budget': budget,
        'current_budget': current_budget,
    })


class BudgetUpdate(LoginRequiredMixin, UpdateView):
    model = Budget
    fields = ['category', 'budget_date', 'budget_amount']
    success_url = '/budget/'


class BudgetDelete(LoginRequiredMixin, DeleteView):
    model = Budget
    success_url = '/budget/'


# All income related views:
# Page to add a form for new income to:
@login_required
def new_income(request):
    income_form = IncomeForm()
    return render(request, 'income/new.html', {
        'income_form': income_form
    })


# New income form (added to the new_income page):
@login_required
def add_income(request):
    income_form = IncomeForm(request.POST)
    if income_form.is_valid():
        new_income_amount = income_form.save(commit=False)
        new_income_amount.user = request.user
        # income_form.instance.user = request.user
        new_income_amount.save()
    return redirect('income_index')


@login_required
def income_index(request):
    income = Income.objects.filter(user=request.user)

    return render(request, 'income/index.html', {
        'income': income,
    })


class IncomeUpdate(LoginRequiredMixin, UpdateView):
    model = Income
    fields = ['income_date', 'income_amount', 'description']
    success_url = '/income/'


class IncomeDelete(LoginRequiredMixin, DeleteView):
    model = Income
    success_url = '/income/'


# All goals related views:
# Page to add a form for new goals to:
@login_required
def new_goal(request):
    goal_form = GoalForm()
    return render(request, 'goals/new.html', {
        'goal_form': goal_form
    })


# New goal form (added to the new_goal page):
@login_required
def add_goal(request):
    goal_form = GoalForm(request.POST)
    if goal_form.is_valid():
        new_goal = goal_form.save(commit=False)
        new_goal.user = request.user
        # goal_form.instance.user = request.user
        new_goal.save()
    return redirect('goal_index')


@login_required
def goal_index(request):
    goals = Goal.objects.filter(user=request.user)

    return render(request, 'goals/index.html', {
        'goals': goals,
    })


class GoalUpdate(LoginRequiredMixin, UpdateView):
    model = Goal
    fields = ['goal_amount', 'goal_date', 'description', 'amount_saved']
    success_url = '/goals/'


class GoalDelete(LoginRequiredMixin, DeleteView):
    model = Goal
    success_url = '/goals/'
