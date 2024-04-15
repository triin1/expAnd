from django.forms import ModelForm
from .models import Category, Subcategory


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class SubcategoryForm(ModelForm):
    class Meta:
        model = Subcategory
        fields = '__all__'