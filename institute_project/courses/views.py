from django.shortcuts import render, redirect
from courses.models import *
from courses.forms import *

def course_category_list(request):
    course_category_data = CourseCategoryModel.objects.all()
    
    context = {
        'course_category_data': course_category_data
    }
    
    return render(request, 'course-category-list.html',context)

def add_category(request):
    form_data = CourseCategoryForm()
    if request.method == 'POST':
        form_data = CourseCategoryForm(request.POST)
        if form_data.is_valid():
            form_data.save()
            return redirect('course_category_list')
    
    context = {
        'form_title': 'Add Course Category Information',
        'form_btn': 'Add Course Category',
        'page_title': 'Add Course Category',
        'form_data': form_data
    }
    return render(request, 'master/base-form.html',context)

def edit_category(request, id):
    data = CourseCategoryModel.objects.get(id = id)
    
    form_data = CourseCategoryForm(instance=data)
    if request.method == 'POST':
        form_data = CourseCategoryForm(request.POST, instance=data)
        if form_data.is_valid():
            form_data.save()
            return redirect('course_category_list')
    
    context = {
        'form_title': 'Edit Course Category Information',
        'form_btn': 'Edit Course Category',
        'page_title': 'Edit Course Category',
        'form_data': form_data
    }
    return render(request, 'master/base-form.html',context)


def delete_category(request, id):
    CourseCategoryModel.objects.get(id = id).delete()
    return redirect('course_category_list')
    
    
def course_list(request):
    course_data = CourseModel.objects.all()
    context = {
        'course_data': course_data
    }
    
    
    return render(request, 'course-list.html',context)

def add_course(request):
    form_data = CourseForm()
    if request.method == 'POST':
        form_data = CourseForm(request.POST, request.FILES)
        if form_data.is_valid():
            course_data = form_data.save(commit=False)
            course_data.created_by = request.user
            course_data.save()
            return redirect('course_list')
    
    context = {
        'form_title': 'Add Course Information',
        'form_btn': 'Add Course',
        'page_title': 'Add Course',
        'form_data': form_data
    }
    return render(request, 'master/base-form.html',context)
    
def edit_course(request, id):
    data = CourseModel.objects.get(id = id)
    form_data = CourseForm(instance=data)
    if request.method == 'POST':
        form_data = CourseForm(request.POST, request.FILES, instance=data)
        if form_data.is_valid():
            course_data = form_data.save(commit=False)
            course_data.created_by = request.user
            course_data.save()
            return redirect('course_list')
    
    context = {
        'form_title': 'Edit Course Information',
        'form_btn': 'Edit Course',
        'page_title': 'Edit Course',
        'form_data': form_data
    }
    return render(request, 'master/base-form.html',context)

def delete_course(request, id):
    CourseModel.objects.get(id = id).delete()
    return redirect('course_list')