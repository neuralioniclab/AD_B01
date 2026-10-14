from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from teachers.models import TeacherModel
from teachers.forms import *
from django.shortcuts import get_object_or_404
from users_auth.decorators import admin_required

# Create your views here.
@admin_required
def teacher_list(request):
    teacher_list = TeacherModel.objects.select_related('user')
    
    context = {
        'teacher_list': teacher_list,
    }
    
    
    return render(request, 'teacher-list.html', context)

@admin_required
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


@admin_required
def edit_teacher(request, id):
    data = get_object_or_404(TeacherModel.objects.select_related('user'), pk=id)
    form_data = TeacherForm(instance=data)
    if request.method == 'POST':
        form_data = TeacherForm(request.POST, request.FILES, instance=data)
        if form_data.is_valid():
            form_data.save()
            messages.success(request, 'Teacher Updated Successfully')
            return redirect('teacher_list')
    return render(request, 'master/base-form.html', {
        'form_data': form_data,
        'form_title': 'Edit Teacher Information',
        'page_title': 'Edit Teacher',
        'form_btn': 'Update Teacher',
    })


@admin_required
def delete_teacher(request, id):
    data = get_object_or_404(TeacherModel, pk=id)
    if request.method == 'POST':
        data.delete()
        messages.success(request, 'Teacher Deleted Successfully')
        return redirect('teacher_list')
    return render(request, 'master/confirm-delete.html', {
        'object': data, 'cancel_url': 'teacher_list',
    })
