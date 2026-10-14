from django.shortcuts import render, redirect
from django.contrib import messages
from students.models import StudentModel
from django.db.models import Q
from students.forms import *
from django.shortcuts import get_object_or_404
from users_auth.decorators import admin_required

# Create your views here.
@admin_required
def student_list(request):
    student_list = StudentModel.objects.select_related('user')
    search_value = request.GET.get('query')
    
    if search_value:
        student_list = student_list.filter(
            Q(roll_no__icontains = search_value) |
            Q(name__icontains = search_value) |
            Q(user__user_type__icontains = search_value)
        )
    
    context = {
        'student_list': student_list,
    }
    
    
    return render(request, 'student-list.html', context)

@admin_required
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


@admin_required
def edit_student(request, id):
    data = get_object_or_404(StudentModel.objects.select_related('user'), pk=id)
    form_data = StudentForm(instance=data)
    if request.method == 'POST':
        form_data = StudentForm(request.POST, request.FILES, instance=data)
        if form_data.is_valid():
            form_data.save()
            messages.success(request, 'Student Updated Successfully')
            return redirect('student_list')
    return render(request, 'master/base-form.html', {
        'form_data': form_data,
        'form_title': 'Edit Student Information',
        'page_title': 'Edit Student',
        'form_btn': 'Update Student',
    })


@admin_required
def delete_student(request, id):
    data = get_object_or_404(StudentModel, pk=id)
    if request.method == 'POST':
        data.delete()
        messages.success(request, 'Student Deleted Successfully')
        return redirect('student_list')
    return render(request, 'master/confirm-delete.html', {
        'object': data, 'cancel_url': 'student_list',
    })
