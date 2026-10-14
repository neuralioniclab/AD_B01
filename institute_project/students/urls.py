from django.urls import path
from students.views import *

urlpatterns = [
    path('edit-student/<int:id>/', edit_student, name='edit_student'),
    path('delete-student/<int:id>/', delete_student, name='delete_student'),
    path('student-list/', student_list, name='student_list'),
    path('add-student/',add_student, name='add_student'),
]
