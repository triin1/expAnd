from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Sum, F, Avg
from django.db.models.functions import TruncMonth, TruncYear
from django.utils import timezone
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Expense, Category, Subcategory, Budget, Income, Goal
from .forms import CategoryForm, SubcategoryForm, ExpenseForm, BudgetForm, IncomeForm, GoalForm
from .utils import get_plot_comparison, get_bar_total, get_pie_current_expenses, get_bar_average, get_bar_daily, get_bar_homemonth, get_bar_homeyear


# All general and authentication related views:
def about(request):
    return render(request, 'about.html')


@login_required
def home(request):
    # Querying all necessary data for the page:
    expenses = Expense.objects.filter(user=request.user)
    budget = Budget.objects.filter(user=request.user)
    income = Income.objects.filter(user=request.user)

    # Simpler version of the total current month expenses, income and budget chart:
    # today = datetime.now()
    # this_month_expenses = expenses.filter(expense_date__month=today.month).aggregate(current_month=Sum('expense_amount'))
    # total_this_month_expenses = float(this_month_expenses['current_month'])
    # this_month_budget = budget.filter(budget_date__month=today.month).aggregate(current_month=Sum('budget_amount'))
    # total_this_month_budget = float(this_month_budget['current_month'])
    # this_month_income = income.filter(income_date__month=today.month).aggregate(current_month=Sum('income_amount'))
    # total_this_month_income = float(this_month_income['current_month'])

    # Defining the first day and the last day of the current month:
    first_day = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    first_day_next_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0) + timedelta(days=32)
    first_day_next_month = first_day_next_month.replace(day=1)
    last_day = first_day_next_month - timedelta(days=1)
    # Calculating current month's expenses and converting necessary data out of that calculation into list to use for bar chart:
    current_expenses = expenses.annotate(month=TruncMonth('expense_date')).values('month').annotate(current_expenses=Sum('expense_amount')).filter(expense_date__gte=first_day, expense_date__lte=last_day)
    total_current_expenses = [float(item['current_expenses']) for item in current_expenses]
    # Calculating current month's budget and converting necessary data out of that calculation into list to use for bar chart:
    current_budget = budget.annotate(month=TruncMonth('budget_date')).values('month').annotate(current_budget=Sum('budget_amount')).filter(budget_date__gte=first_day, budget_date__lte=last_day)
    total_current_budget = [float(item['current_budget']) for item in current_budget]
    # Calculating current month's income and converting necessary data out of that calculation into list to use for bar chart:
    current_income = income.annotate(month=TruncMonth('income_date')).values('month').annotate(current_income=Sum('income_amount')).filter(income_date__gte=first_day, income_date__lte=last_day)
    total_current_income = [float(item['current_income']) for item in current_income]
    # Creating the total expenses, budget and income per current month bar chart:
    x1 = "Expenses"
    y1 = total_current_expenses # total_this_month_expenses
    x2 = "Budget"
    y2 = total_current_budget # total_this_month_budget
    x3 = "Income"
    y3 = total_current_income # total_this_month_income
    chart_bar_home_month = get_bar_homemonth(x1, y1, x2, y2, x3, y3)

    # Calculating total expenses, budget and income for the current year: 
    today = datetime.now()
    this_year_expenses = expenses.filter(expense_date__year=today.year).aggregate(current_year=Sum('expense_amount'))
    total_this_year_expenses = float(this_year_expenses['current_year'])
    this_year_budget = budget.filter(budget_date__year=today.year).aggregate(current_year=Sum('budget_amount'))
    total_this_year_budget = float(this_year_budget['current_year'])
    this_year_income = income.filter(income_date__year=today.year).aggregate(current_year=Sum('income_amount'))
    total_this_year_income = float(this_year_income['current_year'])
    # Creating the total expenses, budget and income per current month bar chart:
    x1 = "Expenses"
    y1 = total_this_year_expenses
    x2 = "Budget"
    y2 = total_this_year_budget
    x3 = "Income"
    y3 = total_this_year_income
    chart_bar_home_year = get_bar_homeyear(x1, y1, x2, y2, x3, y3)

    return render(request, 'home.html', {
        'chart_bar_home_month': chart_bar_home_month,
        'chart_bar_home_year': chart_bar_home_year,
    })


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

    # Define the first day and the last day of the current month:
    first_day = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    first_day_next_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0) + timedelta(days=32)
    first_day_next_month = first_day_next_month.replace(day=1)
    last_day = first_day_next_month - timedelta(days=1)
    # Calculate current month's expenses by category and convert necessary data out of that calculation into lists to use for pie chart:
    current_expenses = expenses.annotate(month=TruncMonth('expense_date'), category_name=F('category__name')).values('month', 'category_name').annotate(current_expenses=Sum('expense_amount')).filter(expense_date__gte=first_day, expense_date__lte=last_day)
    category_names = [item['category_name'] for item in current_expenses]
    totals = [float(item['current_expenses']) for item in current_expenses]
    # Creating the total expenses by category per current month pie chart:
    x = totals
    y = category_names
    chart_pie_current_expenses = get_pie_current_expenses(x, y)

    # Calculate budget and income data for the line chart on total expenses versus income and budget per month:
    monthly_income = income.annotate(month=TruncMonth('income_date')).values('month').order_by('month').annotate(monthly_income=Sum('income_amount'))
    monthly_budget = budget.annotate(month=TruncMonth('budget_date')).values('month').order_by('month').annotate(monthly_budget=Sum('budget_amount'))
    # Create lists out of necessary data (expense data has already been prepared above):
    monthly_incomes = [float(item['monthly_income']) for item in monthly_income]
    monthly_budgets = [float(item['monthly_budget']) for item in monthly_budget]
    months_income = [item['month'] for item in monthly_income]
    months_budget = [item['month'] for item in monthly_budget]
    # Make dictionaries out of the data to get key value pairs where the date/month is the key and monthly amount it the value:
    month_expense_dictionary = {months[i]: expenses_by_month[i] for i in range(len(months))}
    month_budget_dictionary = {months_budget[i]: monthly_budgets[i] for i in range(len(months_budget))}
    month_income_dictionary = {months_income[i]: monthly_incomes[i] for i in range(len(months_income))}
    # Merge all dictionaries. N.B. it does not include full list of all values, it is compiled to get the full range of dates/months only 
    merged_dictionary = {**month_budget_dictionary, **month_income_dictionary, **month_expense_dictionary}
    # Based on the merged dictionaries, define the earliest and latest months that have any entries in any of the three datasets:
    start_month = min(merged_dictionary.keys())
    end_month = max(merged_dictionary.keys())
    # Create a range based on the earliest and latest months that have data:
    month_range = [start_month + relativedelta(months=x) for x in range((end_month.year - start_month.year) * 12 + end_month.month - start_month.month + 1)]
    # Fill in any data gaps in all three datasets by inserting zero values for the months that don't have any data: 
    for month in month_range:
        if month not in month_budget_dictionary:
            month_budget_dictionary[month] = 0
        if month not in month_income_dictionary:
            month_income_dictionary[month] = 0
        if month not in month_expense_dictionary:
            month_expense_dictionary[month] = 0
    # Sort all three datasets based on dates/months:
    sorted_month_expenses = {key: month_expense_dictionary[key] for key in sorted(month_expense_dictionary)}
    sorted_month_income = {key: month_income_dictionary[key] for key in sorted(month_income_dictionary)}
    sorted_month_budget = {key: month_budget_dictionary[key] for key in sorted(month_budget_dictionary)}
    # Break the dictionaries into lists that can be charted. N.B keys maintain the original dictionary order when put into a list; however, the values don't, so different methods have to be used for the keys and values when preparing lists. Turn months into strings for chart presentation:
    sorted_expenses_months_only = list(sorted_month_expenses.keys())
    months_chart_expenses = [date.strftime('%b-%y') for date in sorted_expenses_months_only]
    sorted_income_months_only = list(sorted_month_income.keys())
    months_chart_income = [date.strftime('%b-%y') for date in sorted_income_months_only]
    sorted_budget_months_only = list(sorted_month_budget.keys())
    months_chart_budget = [date.strftime('%b-%y') for date in sorted_budget_months_only]
    monthly_expenses_chart = [month_expense_dictionary[key] for key in sorted_expenses_months_only]
    monthly_income_chart = [month_income_dictionary[key] for key in sorted_income_months_only]
    monthly_budget_chart = [month_budget_dictionary[key] for key in sorted_budget_months_only]
    # Create the line chart for total expenses versus income and budget per month:
    x1 = months_chart_expenses
    x2 = months_chart_income
    x3 = months_chart_budget
    y1 = monthly_expenses_chart
    y2 = monthly_income_chart
    y3 = monthly_budget_chart
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
@login_required
def new_goal(request):
    if request.method == 'POST':
        goal_form = GoalForm(request.POST)
        if goal_form.is_valid():
            new_goal = goal_form.save(commit=False)
            new_goal.user = request.user
            new_goal.save()
            return redirect('goal_index')
    else:
        goal_form = GoalForm()
    return render(request, 'goals/new.html', {
        'goal_form': goal_form
    })


@login_required
def goal_index(request):
    goals = Goal.objects.filter(user=request.user)

    # Calculate goal progress to date: 
    goal_total = goals.values('amount_saved', 'goal_amount')
    goal_amount_list = [float(item['goal_amount']) for item in goal_total]
    goal_progress_list = [float(item['amount_saved']) for item in goal_total]
    goal_progress_calculation = [(i / j)*100 for i, j in zip(goal_progress_list, goal_amount_list)]

    return render(request, 'goals/index.html', {
        'goals': zip(goals, goal_progress_calculation),
    })


class GoalUpdate(LoginRequiredMixin, UpdateView):
    model = Goal
    fields = ['name', 'goal_amount', 'goal_date', 'description', 'amount_saved']
    success_url = '/goals/'


class GoalDelete(LoginRequiredMixin, DeleteView):
    model = Goal
    success_url = '/goals/'
