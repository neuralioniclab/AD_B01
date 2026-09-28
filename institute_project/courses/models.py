from django.db import models
from users_auth.models import UserModel

class CourseCategoryModel(models.Model):
    name = models.CharField(max_length=40)
    
    def __str__(self):
        return f'{self.name}'
    
class CourseModel(models.Model):
    title = models.CharField(max_length=200,null=True)
    description = models.TextField(null=True)
    category = models.ForeignKey(
        CourseCategoryModel,
        on_delete=models.SET_NULL,
        null=True,
        related_name='course_category'
    )
    course_fee = models.FloatField(null=True)
    course_module = models.TextField(null=True)
    course_thumbnail = models.ImageField(upload_to='media/course_img', null=True)
    credit = models.FloatField(null=True)
    created_by = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True, related_name='course_creator')
    
    def __str__(self):
        return f'{self.title}'
    