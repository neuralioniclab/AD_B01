from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from courses.models import *
from courses.forms import *
from users_auth.decorators import admin_required


@admin_required
def course_category_list(request):
    return render(request, 'course-category-list.html', {
        'course_category_data': CourseCategoryModel.objects.all(),
    })


@login_required
def course_list(request):
    course_data = CourseModel.objects.select_related('created_by').prefetch_related('category')
    return render(request, 'course-list.html', {
        'course_data': course_data, 'course_count': course_data.count(),
    })


@login_required
def course_enroll_list(request):
    enrolled_data = CourseEnrollmentModel.objects.select_related('student').prefetch_related('course')
    if request.user.user_type != 'Admin' and not request.user.is_superuser:
        enrolled_data = enrolled_data.filter(student__user=request.user)
    return render(request, 'course-enroll-list.html', {'enrolled_data': enrolled_data})


@login_required
def assign_teacher_list(request):
    assigned_data = AssignTeacherModel.objects.select_related('teacher', 'course')
    if request.user.user_type != 'Admin' and not request.user.is_superuser:
        assigned_data = assigned_data.filter(teacher__user=request.user)
    return render(request, 'assign-teacher-list.html', {'assigned_data': assigned_data})


@admin_required
def add_category(request):
    form_data = CourseCategoryForm()
    if request.method == 'POST':
        form_data = CourseCategoryForm(request.POST)
        if form_data.is_valid():
            form_data.save()
            return redirect('course_category_list')
    return render(request, 'master/base-form.html', {
        'form_title': 'Add Course Category',
        'page_title': 'Add Course Category',
        'form_btn': 'Create',
        'form_data': form_data,
    })


@admin_required
def edit_category(request, id):
    data = get_object_or_404(CourseCategoryModel, pk=id)
    form_data = CourseCategoryForm(instance=data)
    if request.method == 'POST':
        form_data = CourseCategoryForm(request.POST, instance=data)
        if form_data.is_valid():
            form_data.save()
            return redirect('course_category_list')
    return render(request, 'master/base-form.html', {
        'form_title': 'Edit Course Category',
        'page_title': 'Edit Course Category',
        'form_btn': 'Update',
        'form_data': form_data,
    })


@admin_required
def delete_category(request, id):
    data = get_object_or_404(CourseCategoryModel, pk=id)
    if request.method == 'POST':
        data.delete()
        return redirect('course_category_list')
    return render(request, 'master/confirm-delete.html', {
        'object': data, 'cancel_url': 'course_category_list',
    })


@admin_required
def add_course(request):
    form_data = CourseForm()
    if request.method == 'POST':
        form_data = CourseForm(request.POST, request.FILES)
        if form_data.is_valid():
            with transaction.atomic():
                course_data = form_data.save(commit=False)
                course_data.created_by = request.user
                course_data.save()
                form_data.save_m2m()
            return redirect('course_list')
    return render(request, 'master/base-form.html', {
        'form_title': 'Add Course',
        'page_title': 'Add Course',
        'form_btn': 'Create',
        'form_data': form_data,
    })


@admin_required
def edit_course(request, id):
    data = get_object_or_404(CourseModel, pk=id)
    form_data = CourseForm(instance=data)
    if request.method == 'POST':
        form_data = CourseForm(request.POST, request.FILES, instance=data)
        if form_data.is_valid():
            with transaction.atomic():
                course_data = form_data.save(commit=False)
                course_data.save()
                form_data.save_m2m()
            return redirect('course_list')
    return render(request, 'master/base-form.html', {
        'form_title': 'Edit Course',
        'page_title': 'Edit Course',
        'form_btn': 'Update',
        'form_data': form_data,
    })


@admin_required
def delete_course(request, id):
    data = get_object_or_404(CourseModel, pk=id)
    if request.method == 'POST':
        data.delete()
        return redirect('course_list')
    return render(request, 'master/confirm-delete.html', {
        'object': data, 'cancel_url': 'course_list',
    })


@admin_required
def enroll_new_student(request):
    form_data = EnrollStudentForm()
    if request.method == 'POST':
        form_data = EnrollStudentForm(request.POST)
        if form_data.is_valid():
            form_data.save()
            return redirect('course_enroll_list')
    return render(request, 'master/base-form.html', {
        'form_title': 'Add Enrollment',
        'page_title': 'Add Enrollment',
        'form_btn': 'Create',
        'form_data': form_data,
    })


@admin_required
def edit_enrollment(request, id):
    data = get_object_or_404(CourseEnrollmentModel, pk=id)
    form_data = EnrollStudentForm(instance=data)
    if request.method == 'POST':
        form_data = EnrollStudentForm(request.POST, instance=data)
        if form_data.is_valid():
            form_data.save()
            return redirect('course_enroll_list')
    return render(request, 'master/base-form.html', {
        'form_title': 'Edit Enrollment',
        'page_title': 'Edit Enrollment',
        'form_btn': 'Update',
        'form_data': form_data,
    })


@admin_required
def delete_enrollment(request, id):
    data = get_object_or_404(CourseEnrollmentModel, pk=id)
    if request.method == 'POST':
        data.delete()
        return redirect('course_enroll_list')
    return render(request, 'master/confirm-delete.html', {
        'object': data, 'cancel_url': 'course_enroll_list',
    })


@admin_required
def assign_teacher(request):
    form_data = AssignTeacherForm()
    if request.method == 'POST':
        form_data = AssignTeacherForm(request.POST)
        if form_data.is_valid():
            form_data.save()
            return redirect('assign_teacher_list')
    return render(request, 'master/base-form.html', {
        'form_title': 'Add Teacher Assignment',
        'page_title': 'Add Teacher Assignment',
        'form_btn': 'Create',
        'form_data': form_data,
    })


@admin_required
def edit_assignment(request, id):
    data = get_object_or_404(AssignTeacherModel, pk=id)
    form_data = AssignTeacherForm(instance=data)
    if request.method == 'POST':
        form_data = AssignTeacherForm(request.POST, instance=data)
        if form_data.is_valid():
            form_data.save()
            return redirect('assign_teacher_list')
    return render(request, 'master/base-form.html', {
        'form_title': 'Edit Teacher Assignment',
        'page_title': 'Edit Teacher Assignment',
        'form_btn': 'Update',
        'form_data': form_data,
    })


@admin_required
def delete_assignment(request, id):
    data = get_object_or_404(AssignTeacherModel, pk=id)
    if request.method == 'POST':
        data.delete()
        return redirect('assign_teacher_list')
    return render(request, 'master/confirm-delete.html', {
        'object': data, 'cancel_url': 'assign_teacher_list',
    })
