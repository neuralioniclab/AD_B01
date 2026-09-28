from django.contrib import admin
from courses.models import *

admin.site.register([CourseCategoryModel, CourseModel])
