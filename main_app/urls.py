from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('categories/', views.category_index, name="category_index"),
    path('categories/add_category/', views.add_category, name='add_category'),
    path('categories/add_subcategory/', views.add_subcategory, name='add_subcategory'),
    path('categories/<int:pk>/update/', views.CategoryUpdate.as_view(), name='update_category'),
    path('categories/<int:pk>/sub_update/', views.SubcategoryUpdate.as_view(), name='update_subcategory'),
    path('categories/<int:pk>/delete/', views.CategoryDelete.as_view(), name='delete_category'),
    path('categories/<int:pk>/sub_delete/', views.SubcategoryDelete.as_view(), name='delete_subcategory'),

    path('expenses/', views.expenses_index, name="expense_index"),
    path('expenses/detail/', views.expenses_detail, name="expense_detail"),
    path('expenses/add/', views.add_expense, name='add_expense'),
    path('expenses/<int:pk>/update/', views.ExpenseUpdate.as_view(), name='update_expense'),
    path('expenses/<int:pk>/delete/', views.ExpenseDelete.as_view(), name='delete_expense'),
]