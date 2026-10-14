import base64
import shutil
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from courses.models import CourseCategoryModel, CourseModel, CourseEnrollmentModel, AssignTeacherModel
from students.models import StudentModel
from teachers.models import TeacherModel
from users_auth.models import UserModel


class InstituteCRUDTests(TestCase):
    def setUp(self):
        media = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, media)
        settings = override_settings(MEDIA_ROOT=media)
        settings.enable()
        self.addCleanup(settings.disable)
        self.admin = UserModel.objects.create_user(username='admin', user_type='Admin')
        self.client.force_login(self.admin)
        self.category = CourseCategoryModel.objects.create(name='Programming')
        self.course = CourseModel.objects.create(title='Python', course_fee=100, created_by=self.admin)
        self.course.category.add(self.category)
        self.other_course = CourseModel.objects.create(title='Django', course_fee=200)
        self.student_user = UserModel.objects.create_user(username='student', user_type='Student')
        self.student = StudentModel.objects.create(user=self.student_user, name='Student')
        self.teacher_user = UserModel.objects.create_user(username='teacher', user_type='Teacher')
        self.teacher = TeacherModel.objects.create(user=self.teacher_user, name='Teacher')

    def image(self):
        return SimpleUploadedFile('photo.gif', base64.b64decode(
            'R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7'
        ), content_type='image/gif')

    def test_course_create_update_saves_categories_and_creator(self):
        payload = {
            'title': 'New Course', 'description': 'Description', 'category': [self.category.pk],
            'course_fee': 400, 'course_module': 'Module', 'credit': 3,
            'course_thumbnail': self.image(),
        }
        self.assertEqual(self.client.post(reverse('add_course'), payload).status_code, 302)
        course = CourseModel.objects.get(title='New Course')
        self.assertEqual(list(course.category.all()), [self.category])
        other = CourseCategoryModel.objects.create(name='Web')
        payload.pop('course_thumbnail')
        payload['category'] = [other.pk]
        payload['title'] = 'Updated Course'
        self.assertEqual(self.client.post(reverse('edit_course', args=[course.pk]), payload).status_code, 302)
        course.refresh_from_db()
        self.assertEqual(course.created_by, self.admin)
        self.assertEqual(list(course.category.all()), [other])

    def test_enrollment_create_update_calculates_multiple_course_fees(self):
        payload = {'student': self.student.pk, 'course': [self.course.pk, self.other_course.pk], 'pay': 50}
        self.assertEqual(self.client.post(reverse('enroll_new_student'), payload).status_code, 302)
        enrollment = CourseEnrollmentModel.objects.get()
        self.assertEqual(enrollment.course.count(), 2)
        self.assertEqual((enrollment.admission_fee, enrollment.due), (300, 250))
        payload.update(course=[self.other_course.pk], pay=100)
        self.assertEqual(self.client.post(reverse('edit_enrollment', args=[enrollment.pk]), payload).status_code, 302)
        enrollment.refresh_from_db()
        self.assertEqual((enrollment.admission_fee, enrollment.due), (200, 100))
        self.assertEqual(list(enrollment.course.all()), [self.other_course])

    def test_category_and_assignment_create_update(self):
        self.assertEqual(self.client.post(reverse('add_category'), {'name': 'Science'}).status_code, 302)
        category = CourseCategoryModel.objects.get(name='Science')
        self.assertEqual(self.client.post(reverse('edit_category', args=[category.pk]), {'name': 'Math'}).status_code, 302)
        category.refresh_from_db()
        self.assertEqual(category.name, 'Math')
        payload = {'teacher': self.teacher.pk, 'course': self.course.pk}
        self.assertEqual(self.client.post(reverse('assign_teacher'), payload).status_code, 302)
        assignment = AssignTeacherModel.objects.get()
        payload['course'] = self.other_course.pk
        self.assertEqual(self.client.post(reverse('edit_assignment', args=[assignment.pk]), payload).status_code, 302)
        assignment.refresh_from_db()
        self.assertEqual(assignment.course, self.other_course)

    def test_profile_create_update_preserves_account_and_password(self):
        for kind, model in [('student', StudentModel), ('teacher', TeacherModel)]:
            with self.subTest(kind=kind):
                payload = {
                    'username': 'new_' + kind, 'email': 'new@example.com',
                    'name': 'New Person', 'address': 'Dhaka', 'phone': '012345',
                    'image': self.image(), 'roll_no': '12',
                    'employee_id': 'E12', 'designation': 'Lecturer',
                }
                self.assertEqual(self.client.post(reverse('add_' + kind), payload).status_code, 302)
                profile = model.objects.get(user__username='new_' + kind)
                user_id, password = profile.user_id, profile.user.password
                payload.pop('image')
                payload.update(username='updated_' + kind, email='updated@example.com')
                count = UserModel.objects.count()
                self.assertEqual(self.client.post(reverse('edit_' + kind, args=[profile.pk]), payload).status_code, 302)
                profile.refresh_from_db()
                self.assertEqual(profile.user_id, user_id)
                self.assertEqual(profile.user.username, 'updated_' + kind)
                self.assertEqual(profile.user.password, password)
                self.assertEqual(UserModel.objects.count(), count)
                payload['username'] = 'admin'
                response = self.client.post(reverse('edit_' + kind, args=[profile.pk]), payload)
                self.assertEqual(response.status_code, 200)
                self.assertIn('username', response.context['form_data'].errors)

    def test_lists_render_and_related_queries_are_bounded(self):
        enrollment = CourseEnrollmentModel.objects.create(student=self.student, pay=0)
        enrollment.course.add(self.course)
        AssignTeacherModel.objects.create(teacher=self.teacher, course=self.course)
        for name in ['student_list', 'teacher_list', 'course_category_list', 'course_list',
                     'course_enroll_list', 'assign_teacher_list']:
            self.assertEqual(self.client.get(reverse(name)).status_code, 200)
        with self.assertNumQueries(2):
            courses = list(CourseModel.objects.select_related('created_by').prefetch_related('category'))
            for course in courses:
                list(course.category.all())
                course.created_by
        with self.assertNumQueries(2):
            enrollments = list(CourseEnrollmentModel.objects.select_related('student').prefetch_related('course'))
            for row in enrollments:
                row.student.name
                list(row.course.all())
        with self.assertNumQueries(1):
            for row in AssignTeacherModel.objects.select_related('teacher', 'course'):
                row.teacher.name
                row.course.title

    def test_delete_requires_confirmation_and_missing_records_return_404(self):
        enrollment = CourseEnrollmentModel.objects.create(student=self.student)
        assignment = AssignTeacherModel.objects.create(teacher=self.teacher, course=self.course)
        for kind, obj in [('enrollment', enrollment), ('assignment', assignment),
                          ('course', self.course), ('category', self.category),
                          ('student', self.student), ('teacher', self.teacher)]:
            url = reverse('delete_' + kind, args=[obj.pk])
            self.assertEqual(self.client.get(url).status_code, 200)
            self.assertTrue(type(obj).objects.filter(pk=obj.pk).exists())
            self.assertEqual(self.client.post(url).status_code, 302)
            self.assertFalse(type(obj).objects.filter(pk=obj.pk).exists())
            self.assertEqual(self.client.post(url).status_code, 404)

    def test_role_access_and_missing_profiles(self):
        own = CourseEnrollmentModel.objects.create(student=self.student)
        other_student = StudentModel.objects.create(name='Other')
        CourseEnrollmentModel.objects.create(student=other_student)
        self.client.force_login(self.student_user)
        response = self.client.get(reverse('course_enroll_list'))
        self.assertEqual(list(response.context['enrolled_data']), [own])
        self.assertEqual(self.client.get(reverse('add_course')).status_code, 403)
        self.assertEqual(self.client.post(reverse('delete_course', args=[self.course.pk])).status_code, 403)
        self.assertEqual(self.client.get(reverse('assign_teacher_list')).status_code, 200)
        self.client.force_login(self.teacher_user)
        self.assertEqual(self.client.get(reverse('course_enroll_list')).status_code, 200)
        self.client.logout()
        self.assertEqual(self.client.get(reverse('course_list')).status_code, 302)
