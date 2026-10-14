from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
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
    # course_data = CourseModel.objects.all()
    course_data = CourseModel.objects.select_related('category')
    new_data = CourseModel.objects.filter(title__startswith = 'Ad')
    
    another_data = CourseCategoryModel.objects.prefetch_related('course_category')
    
    
    context = {
        'course_data': course_data,
        'new_data': new_data,
        'course_count': course_data.count(),
        'another_data': another_data
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
    # data = get_object_or_404(CourseModel, id = id)
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


def course_enroll_list(request):
    if request.user.user_type == 'Admin':
        data = CourseEnrollmentModel.objects.all()
        print(data.count())
        enrolled_data = CourseEnrollmentModel.objects.prefetch_related('student_courses')
        
    else:
        
        enrolled_data = CourseEnrollmentModel.objects.filter(student=request.user.student_profile)
    context = {
        'enrolled_ata' : enrolled_data
    }
    
    return render(request, 'course-enroll-list.html', context)

def enroll_new_student(request):
    form_data = EnrollStudentForm()
    if request.method == 'POST':
        form_data = EnrollStudentForm(request.POST)
        if form_data.is_valid():
            enroll_from = form_data.save(commit=False)
            # enroll_from.admission_fee = enroll_from.course.course_fee
            # enroll_from.due = enroll_from.course.course_fee - enroll_from.pay
            enroll_from.save()
            
            return redirect('course_enroll_list')
    
    context = {
        'form_title': 'Enroll New Student Info',
        'form_btn': 'Enroll New Student ',
        'page_title': 'Enroll New Student',
        'form_data': form_data
    }
    
    
    return render(request, 'master/base-form.html', context)


def assign_teacher_list(request):
    if request.user.user_type == 'Admin':
        assigned_data = AssignTeacherModel.objects.all()
    else:
        assigned_data = AssignTeacherModel.objects.filter(teacher = request.user.teacher_profile)
    context = {
        'assigned_data' : assigned_data
    }
    
    return render(request, 'assign-teacher-list.html', context)

def assign_teacher(request):
    form_data = AssignTeacherForm()
    if request.method == 'POST':
        form_data = AssignTeacherForm(request.POST)
        if form_data.is_valid():
            form_data.save()
            return redirect('assign_teacher_list')
    
    context = {
        'form_title': 'Assign Teacher Info',
        'form_btn': 'Assign Teacher ',
        'page_title': 'Assign Teacher',
        'form_data': form_data
    }
    
    
    return render(request, 'master/base-form.html', context)