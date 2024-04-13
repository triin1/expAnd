from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # path('expenses/create', views.ExpenseCreate.as_views, name='expense_create'),
]