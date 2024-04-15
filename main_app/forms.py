from django.forms import ModelForm
from .models import Subcategory

class SubcategoryForm(ModelForm):
    class Meta:
        model = Subcategory
        fields = '__all__'