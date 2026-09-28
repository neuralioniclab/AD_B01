from django.shortcuts import render, redirect
from django.contrib import messages
from students.models import StudentModel
from students.forms import *

# Create your views here.
def student_list(request):
    student_list = StudentModel.objects.all()
    
    context = {
        'student_list': student_list,
    }
    
    
    return render(request, 'student-list.html', context)

def add_student(request):
    
    form_data = StudentForm()
    if request.method == 'POST':
        form_data = StudentForm(request.POST, request.FILES)
        if form_data.is_valid():
            form_data.save()
            messages.success(request, 'Student Register Successfully')
            return redirect('student_list')
        
    context = {
        'form_title': 'Add Student Information',
        'form_btn': 'Add Student',
        'page_title': 'Student Register',
        'form_data': form_data
    }
    
    return render(request, 'master/base-form.html', context)