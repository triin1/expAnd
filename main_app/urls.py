from django.urls import path
from . import views

urlpatterns = [
    # all general paths:
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    
    # all authentication paths:
    path('accounts/signup/', views.signup, name='signup'),

    # all paths related to categories:
    path('categories/', views.category_index, name="category_index"),
    path('categories/add_category/', views.add_category, name='add_category'),
    path('categories/add_subcategory/', views.add_subcategory, name='add_subcategory'),
    path('categories/<int:pk>/update/', views.CategoryUpdate.as_view(), name='update_category'),
    path('categories/<int:pk>/sub_update/', views.SubcategoryUpdate.as_view(), name='update_subcategory'),
    path('categories/<int:pk>/delete/', views.CategoryDelete.as_view(), name='delete_category'),
    path('categories/<int:pk>/sub_delete/', views.SubcategoryDelete.as_view(), name='delete_subcategory'),

    # all paths related to expenses:
    path('expenses/new', views.expenses_new, name="expense_new"),
    path('expenses/detail/', views.expenses_detail, name="expense_detail"),
    path('expenses/<int:pk>/update/', views.ExpenseUpdate.as_view(), name='update_expense'),
    path('expenses/<int:pk>/delete/', views.ExpenseDelete.as_view(), name='delete_expense'),
    path('expenses/summary/', views.summary_index, name='summary_index'),

    # all paths related to budget:
    path('budget/', views.budget_index, name="budget_index"),
    path('budget/add/', views.add_budget_amount, name='add_budget_amount'),
    path('budget/<int:pk>/update/', views.BudgetUpdate.as_view(), name='update_budget'),
    path('budget/<int:pk>/delete/', views.BudgetDelete.as_view(), name='delete_budget'),

    # all paths related to income:
    path('income/new/', views.new_income, name="new_income"),
    path('income/', views.income_index, name="income_index"),
    path('income/<int:pk>/update/', views.IncomeUpdate.as_view(), name='update_income'),
    path('income/<int:pk>/delete/', views.IncomeDelete.as_view(), name='delete_income'),

    # all paths related to goals:
    path('goals/new/', views.new_goal, name="new_goal"),
    path('goals/', views.goal_index, name="goal_index"),
    path('goals/<int:pk>/update/', views.GoalUpdate.as_view(), name='update_goal'),
    path('goals/<int:pk>/delete/', views.GoalDelete.as_view(), name='delete_goal'),
]