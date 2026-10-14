from django.urls import path
from courses.views import *

urlpatterns = [
    path('edit-enrollment/<int:id>/', edit_enrollment, name='edit_enrollment'),
    path('delete-enrollment/<int:id>/', delete_enrollment, name='delete_enrollment'),
    path('edit-assignment/<int:id>/', edit_assignment, name='edit_assignment'),
    path('delete-assignment/<int:id>/', delete_assignment, name='delete_assignment'),
    #-------Course Category Url
    path('course-category/', course_category_list, name='course_category_list'),
    path('add_category/',add_category, name='add_category'),
    path('edit_category/<str:id>/',edit_category, name='edit_category'),
    path('delete-category/<str:id>/',delete_category, name='delete_category'),
    
    #--------Course Url
    path('course-list/',course_list, name='course_list'),
    path('add_course/',add_course, name='add_course'),
    path('edit_course/<str:id>/',edit_course, name='edit_course'),
    path('delete-course/<str:id>/',delete_course, name='delete_course'),
    
    #---Enrollment
    path('course-enroll-list/',course_enroll_list, name='course_enroll_list'),
    path('enroll-new-student/',enroll_new_student, name='enroll_new_student'),
    
    path('assign-teacher-list/',assign_teacher_list, name='assign_teacher_list'),
    path('assign_teacher/', assign_teacher, name='assign_teacher'),
]
