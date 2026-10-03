from django import forms
from django.db import transaction
from teachers.models import *
from users_auth.models import UserModel

class TeacherForm(forms.ModelForm):
    username = forms.CharField(max_length=200)
    email = forms.EmailField()
    
    class Meta:
        model = TeacherModel
        fields = '__all__'
        exclude = ['user']
    
    @transaction.atomic  
    def save(self, commit = True):
        user = UserModel.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password='123456',
            user_type = 'Teacher'
        )
        teacher =  super().save(commit=False)
        teacher.user = user
        if commit:
            teacher.save()
        return teacher