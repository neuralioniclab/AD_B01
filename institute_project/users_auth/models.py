from django.db import models
from django.contrib.auth.models import AbstractUser


class UserModel(AbstractUser):
    USER_TYPES = [
        ('Admin','Admin'),
        ('Teacher','Teacher'),
        ('Student','Student'),
    ]
    user_type = models.CharField(choices=USER_TYPES, max_length=20, null=True)
    
    def __str__(self):
        return f'{self.username}'
    
class BasicInfoModel(models.Model):
    name = models.CharField(max_length=200, null=True)
    address = models.TextField(null=True)
    phone = models.CharField(max_length=20, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    

    
    
class TeacherModel(BasicInfoModel):
    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        related_name='teacher_profile',
        null=True
    )
    joining_date = models.DateField(null=True)
    image = models.ImageField(upload_to='media/teacher_img', null=True)
    
    def __str__(self):
            return f'{self.user.username}'