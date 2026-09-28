from django.urls import path
from courses.views import *

urlpatterns = [
    #-------Course Category Url
    path('course-category/', course_category_list, name='course_category_list'),
    path('add_category/',add_category, name='add_category'),
    path('edit_category/<str:id>/',edit_category, name='edit_category'),
    path('delete-category/<str:id>/',delete_category, name='delete_category'),
    
    #--------Course Url
    path('course-list/',course_list, name='course_list'),
    path('add_course/',add_course, name='add_course'),
    path('edit_course/<str:id>/',edit_course, name='edit_course'),
    path('delete-course/<str:id>/',delete_course, name='delete_course')
]