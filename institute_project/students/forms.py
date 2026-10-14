from django import forms
from django.db import transaction
from students.models import *
from users_auth.models import UserModel

class StudentForm(forms.ModelForm):
    username = forms.CharField(max_length=200)
    email = forms.EmailField()
    
    class Meta:
        model = StudentModel
        fields = '__all__'
        exclude = ['user']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.user_id:
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email

    def clean_username(self):
        username = self.cleaned_data['username']
        users = UserModel.objects.filter(username=username)
        if self.instance.user_id:
            users = users.exclude(pk=self.instance.user_id)
        if users.exists():
            raise forms.ValidationError('This username is already in use.')
        return username

    @transaction.atomic
    def save(self, commit = True):
        student =  super().save(commit=False)
        user = student.user if student.user_id else UserModel(user_type='Student')
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        if not user.pk:
            user.set_password('123456')
        student.user = user
        if commit:
            user.save()
            student.user = user
            student.save()
        return student
