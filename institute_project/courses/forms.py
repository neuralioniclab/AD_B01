from django import forms
from courses.models import *

class CourseCategoryForm(forms.ModelForm):
    class Meta:
        model = CourseCategoryModel
        fields = '__all__'
        
class CourseForm(forms.ModelForm):
    class Meta:
        model = CourseModel
        fields = '__all__'
        exclude = ['created_by']