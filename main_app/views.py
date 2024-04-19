from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Sum, F, Avg
from django.db.models.functions import TruncMonth, TruncYear
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Expense, Category, Subcategory, Budget, Income, Goal
from .forms import CategoryForm, SubcategoryForm, ExpenseForm, BudgetForm, IncomeForm, GoalForm
from .utils import get_plot_comparison, get_bar_total, get_pie_current_expenses, get_bar_average, get_bar_daily


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
    # Querying all necessary data for the page:
    expenses = Expense.objects.filter(user=request.user)
    budget = Budget.objects.filter(user=request.user)
    income = Income.objects.filter(user=request.user)

    # Calculating data for the bar chart on total expenses per month:
    expense_by_month = expenses.annotate(month=TruncMonth('expense_date'), year=TruncYear('expense_date')).values('month', 'year').order_by('month').annotate(expense_by_month=Sum('expense_amount'))
    # Creating lists of calculated data to use for charting:
    expenses_by_month = [float(item['expense_by_month']) for item in expense_by_month]
    months = [item['month'] for item in expense_by_month]
    # Converting date (month and year) into string:
    month_year = [date.strftime('%b-%y') for date in months]
    # Creating the total expenses per month bar chart:
    x = month_year
    y = expenses_by_month
    chart_bar_total_expenses = get_bar_total(x, y)

    # Defining the first day and the last day of the current month:
    first_day = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    first_day_next_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0) + timedelta(days=32)
    first_day_next_month = first_day_next_month.replace(day=1)
    last_day = first_day_next_month - timedelta(days=1)
    # Calculating current month's expenses by category and converting necessary data out of that calculation into lists to use for pie chart:
    current_expenses = expenses.annotate(month=TruncMonth('expense_date'), category_name=F('category__name')).values('month', 'category_name').annotate(current_expenses=Sum('expense_amount')).filter(expense_date__gte=first_day, expense_date__lte=last_day)
    category_names = [item['category_name'] for item in current_expenses]
    totals = [float(item['current_expenses']) for item in current_expenses]
    # Creating the total expenses by category per current month pie chart:
    x = totals
    y = category_names
    chart_pie_current_expenses = get_pie_current_expenses(x, y)

    # Calculating budget and income data for the line chart on total expenses versus income and budget per month:
    monthly_income = income.annotate(month=TruncMonth('income_date'), year=TruncYear('income_date')).values('month', 'year').order_by('month').annotate(monthly_income=Sum('income_amount'))
    monthly_budget = budget.annotate(month=TruncMonth('budget_date'), year=TruncYear('budget_date')).values('month', 'year').order_by('month').annotate(monthly_budget=Sum('budget_amount'))
    # Creating lists out of necessary data for plotting on the chart:
    monthly_incomes = [float(item['monthly_income']) for item in monthly_income]
    monthly_budgets = [float(item['monthly_budget']) for item in monthly_budget]
    months_income = [item['month'] for item in monthly_income]
    months_budget = [item['month'] for item in monthly_budget]
    # Converting dates (month and year) into strings:
    month_year_income = [date.strftime('%b-%y') for date in months_income]
    month_year_budget = [date.strftime('%b-%y') for date in months_budget]
    # # Creating the line chart on total expenses versus income and budget per month:
    x1 = month_year
    x2 = month_year_income
    x3 = month_year_budget
    y1 = expenses_by_month
    y2 = monthly_incomes
    y3 = monthly_budgets
    chart_plot_comparison = get_plot_comparison(x1, y1, x2, y2, x3, y3)

    # Monthly average spend - calculating and making data lists for the bar chart:
    monthly_average_expense = expenses.annotate(month=TruncMonth('expense_date')).values('month').order_by('month').annotate(average_by_month=Avg('expense_amount'))
    monthly_average_expenses = [float(item['average_by_month']) for item in monthly_average_expense]
    months_average = [item['month'] for item in monthly_average_expense]
    month_year_average = [date.strftime('%b-%y') for date in months_average]
    # Creating the average expenses per month bar chart:
    x = month_year_average
    y = monthly_average_expenses
    chart_bar_average_expenses = get_bar_average(x, y)

    # Calculate daily total expense amounts
    daily_totals = expenses.values('expense_date').order_by('expense_date').annotate(daily_totals=Sum('expense_amount'))
    # Extract daily total expense amounts and dates into two lists and then merge them into one dictionary
    dates = [item['expense_date'] for item in daily_totals]
    daily_total = [float(item['daily_totals']) for item in daily_totals]
    daily_total_dictionary = {dates[i]: daily_total[i] for i in range(len(dates))}
    # Enter missing dates to the dataset with zero values:
    start_date = min(daily_total_dictionary.keys())
    end_date = max(daily_total_dictionary.keys())
    date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]
    for date in date_range:
        if date not in daily_total_dictionary:
            daily_total_dictionary[date] = 0
    # Break the dictionary into two lists that can be charted:
    days_chart = list(daily_total_dictionary.keys())
    daily_expenses_chart = list(daily_total_dictionary.values())
    # Create the daily expenses chart:
    x1 = days_chart
    y1 = daily_expenses_chart
    chart_daily = get_bar_daily(x1, y1)

    # Calculating total expenses by category and by month and order the expenses by month with most recent at the top (diaplayed as a table on the page):
    total_expenses = expenses.annotate(month=TruncMonth('expense_date'), category_name=F('category__name')).order_by('-month').values('month', 'category_name').annotate(total_expenses=Sum('expense_amount'))

    return render(request, 'expenses/summary.html', {
        'expenses': expenses,
        'total_expenses': total_expenses,
        'chart_bar_total_expenses': chart_bar_total_expenses,
        'chart_pie_current_expenses': chart_pie_current_expenses,
        'chart_plot_comparison': chart_plot_comparison,
        'chart_bar_average_expenses': chart_bar_average_expenses,
        'chart_daily': chart_daily, 
    })


# All budget related views:
@login_required
def add_budget_amount(request):
    budget_form = BudgetForm(request.user, request.POST)
    if budget_form.is_valid():
        new_budget_amount = budget_form.save(commit=False)
        new_budget_amount.user = request.user
        new_budget_amount.save()
    return redirect('budget_index')


@login_required
def budget_index(request):
    budget = Budget.objects.filter(user=request.user)
    budget_form = BudgetForm(user=request.user)
    expenses = Expense.objects.filter(user=request.user)

    # Defining the first day and the last day of the current month:
    first_day = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    first_day_next_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0) + timedelta(days=32)
    first_day_next_month = first_day_next_month.replace(day=1)
    last_day = first_day_next_month - timedelta(days=1)

    # Calculating the current month's budget amounts by category. The annotate defines calculation parameters of month and category name
    # and sums up the budget amounts based on these parameters. Filter uses first and last day of the month to filter out the sums by
    # category only for the current month:
    current_budget = budget.annotate(month=TruncMonth('budget_date'), category_name=F('category__name')).values('month', 'category_name').annotate(current_budget=Sum('budget_amount')).filter(budget_date__gte=first_day, budget_date__lte=last_day)

    # Perform the same calculation as above, but for current month's expenses:
    current_expenses = expenses.annotate(month=TruncMonth('expense_date'), category_name=F('category__name')).values('month', 'category_name').annotate(current_expenses=Sum('expense_amount')).filter(expense_date__gte=first_day, expense_date__lte=last_day)

    # Calculating the difference between the budget and expenses in the current month:
    budget_delta = [float(item['current_budget']) for item in current_budget]
    expense_delta = [float(item['current_expenses']) for item in current_expenses]
    current_delta = [budget_delta[i] - expense_delta[i] for i in range(min(len(budget_delta), len(expense_delta)))]

    return render(request, 'budget/index.html', {
        'budget_form': budget_form,
        'budget': budget,
        'current_data': zip(current_budget, current_expenses, current_delta)
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
