from django.urls import path
from teachers.views import *

urlpatterns = [
    path('edit-teacher/<int:id>/', edit_teacher, name='edit_teacher'),
    path('delete-teacher/<int:id>/', delete_teacher, name='delete_teacher'),
    path('teacher-list/', teacher_list, name='teacher_list'),
    path('add-teacher/',add_teacher, name='add_teacher'),
]
