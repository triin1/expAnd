from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('categories/', views.category_index, name="category_index"),
    path('categories/add_category/', views.add_category, name='add_category'),
    path('categories/add_subcategory', views.add_subcategory, name='add_subcategory'),

    path('expenses/create/', views.ExpenseCreate.as_view(), name='expense_create'),
]