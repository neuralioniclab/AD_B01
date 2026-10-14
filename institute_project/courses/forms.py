from django import forms
from django.db import transaction
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
        
class EnrollStudentForm(forms.ModelForm):
    class Meta:
        model = CourseEnrollmentModel
        fields = '__all__'
        exclude = ['admission_fee','due']

    @transaction.atomic
    def save(self, commit=True):
        enrollment = super().save(commit=False)
        enrollment.admission_fee = sum(course.course_fee or 0 for course in self.cleaned_data['course'])
        enrollment.due = enrollment.admission_fee - (enrollment.pay or 0)
        if commit:
            enrollment.save()
            self.save_m2m()
        return enrollment
    
    
class AssignTeacherForm(forms.ModelForm):
    class Meta:
        model = AssignTeacherModel
        fields = '__all__'
