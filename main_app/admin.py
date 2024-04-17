from django.contrib import admin
from .models import Expense, Category, Subcategory, Budget

admin.site.register(Expense)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Budget)
