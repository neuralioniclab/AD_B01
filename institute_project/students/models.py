from django.db import models
from users_auth.models import BasicInfoModel, UserModel

# Create your models here.
class StudentModel(BasicInfoModel):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='student_profile', null=True)
    roll_no = models.CharField(max_length=20, null=True)
    image = models.ImageField(upload_to='media/student_img', null=True)
    
    def __str__(self):
            return f'{self.user.username}'