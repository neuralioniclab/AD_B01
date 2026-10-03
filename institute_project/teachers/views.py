from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from teachers.models import TeacherModel
from teachers.forms import *

# Create your views here.
def teacher_list(request):
    teacher_list = TeacherModel.objects.all()
    
    context = {
        'teacher_list': teacher_list,
    }
    
    
    return render(request, 'teacher-list.html', context)

def add_teacher(request):
    
    form_data = TeacherForm()
    if request.method == 'POST':
        form_data = TeacherForm(request.POST, request.FILES)
        if form_data.is_valid():
            form_data.save()
            messages.success(request, 'Teacher Register Successfully')
            return redirect('teacher_list')
        
    context = {
        'form_title': 'Add Teacher Information',
        'form_btn': 'Add Teacher',
        'page_title': 'Teacher Register',
        'form_data': form_data
    }
    
    return render(request, 'master/base-form.html', context)