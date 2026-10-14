from django.db import models
from users_auth.models import BasicInfoModel, UserModel

# Create your models here.
class TeacherModel(BasicInfoModel):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='teacher_profile', null=True)
    employee_id = models.CharField(max_length=20, null=True)
    designation = models.CharField(max_length=100, null=True)
    image = models.ImageField(upload_to='media/teacher_img', null=True)

    def __str__(self):
        return self.name or (self.user.username if self.user_id else 'Teacher')
