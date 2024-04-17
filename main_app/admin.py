from django.contrib import admin
from .models import Expense, Category, Subcategory, Budget, Income, Goal

admin.site.register(Expense)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Budget)
admin.site.register(Income)
admin.site.register(Goal)
