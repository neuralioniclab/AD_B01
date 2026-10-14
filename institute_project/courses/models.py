from django.db import models
from teachers.models import TeacherModel
from students.models import StudentModel
from users_auth.models import UserModel

class CourseCategoryModel(models.Model):
    name = models.CharField(max_length=40)
    # Python, JS
    
    def __str__(self):
        return f'{self.name}'
    
class CourseModel(models.Model):
    title = models.CharField(max_length=200,null=True)
    description = models.TextField(null=True)
    category = models.ManyToManyField(
        CourseCategoryModel,
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


class CourseEnrollmentModel(models.Model):
    student = models.ForeignKey(StudentModel, on_delete=models.SET_NULL, null=True, related_name='student_enrollment')
    course = models.ManyToManyField(CourseModel, related_name='student_courses')
    admission_fee = models.FloatField(null=True)
    pay = models.FloatField(null=True)
    due = models.FloatField(null=True)
    
    
    def __str__(self):
        return (self.student.name or 'Student') if self.student_id else 'Deleted student'
    
    # def save(self, *args, **kwargs):
    #     self.admission_fee = self.course.course_fee
    #     self.due = self.admission_fee - self.pay
    #     super().save(*args, **kwargs)
        

class AssignTeacherModel(models.Model):
    teacher = models.ForeignKey(TeacherModel, on_delete= models.SET_NULL, related_name='assign_course', null=True)
    course = models.ForeignKey(
        CourseModel,
        on_delete=models.CASCADE,
        null=True
    )
    def __str__(self):
        teacher = self.teacher.name if self.teacher_id else 'Deleted teacher'
        course = self.course.title if self.course_id else 'Deleted course'
        return f'{teacher}-{course}'
