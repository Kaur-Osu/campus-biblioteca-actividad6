import secrets
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken
User = get_user_model()
class SecurityTests(APITestCase):
    def setUp(self):
        self.admin_password = secrets.token_urlsafe(24)
        self.student_password = secrets.token_urlsafe(24)
        self.new_password = secrets.token_urlsafe(24)
        self.admin = User.objects.create_superuser(username='admin',email='admin@campus.test',matricula='ADMIN',password=self.admin_password)
        self.student = User.objects.create_user(username='alumno',email='alumno@campus.test',matricula='UT001',password=self.student_password)
    def login(self, user):
        r=self.client.post('/api/v1/auth/token/',{'email':user.email,'password':self.admin_password if user.is_staff else self.student_password})
        self.assertEqual(r.status_code,200)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+r.data['access'])
        return r
    def test_email_login_and_token_lifetime(self):
        r=self.login(self.student)
        token=AccessToken(r.data['access'])
        self.assertEqual(token['exp']-token['iat'],900)
    def test_me_requires_token_and_hides_password(self):
        self.assertEqual(self.client.get('/api/v1/auth/me/').status_code,401)
        self.login(self.student)
        r=self.client.get('/api/v1/auth/me/')
        self.assertEqual(r.status_code,200)
        self.assertNotIn('password',r.data)
        self.assertEqual(r.data['matricula'],'UT001')
    def test_student_cannot_manage_users(self):
        self.login(self.student)
        self.assertEqual(self.client.get('/api/v1/users/').status_code,403)
        self.assertEqual(self.client.patch(f'/api/v1/users/{self.admin.pk}/',{'is_staff':True}).status_code,403)
    def test_patch_without_password_keeps_target_hash(self):
        self.login(self.admin)
        before=self.student.password
        r=self.client.patch(f'/api/v1/users/{self.student.pk}/',{'first_name':'Carlos'})
        self.assertEqual(r.status_code,200)
        self.student.refresh_from_db()
        self.assertEqual(before,self.student.password)
        self.assertTrue(self.student.check_password(self.student_password))
        self.assertFalse(self.student.check_password(self.admin_password))
        self.assertNotIn('password',r.data)
    def test_put_without_password_keeps_target_hash(self):
        self.login(self.admin)
        before=self.student.password
        r=self.client.put(f'/api/v1/users/{self.student.pk}/',{'username':'alumno','email':'alumno@campus.test','matricula':'UT001','first_name':'Actualizado'})
        self.assertEqual(r.status_code,200)
        self.student.refresh_from_db()
        self.assertEqual(before,self.student.password)
        self.assertNotIn('password',r.data)
    def test_explicit_password_change_and_empty_rejection(self):
        self.login(self.admin)
        url=f'/api/v1/users/{self.student.pk}/'
        self.assertEqual(self.client.patch(url,{'password':''}).status_code,400)
        r=self.client.patch(url,{'password':self.new_password})
        self.assertEqual(r.status_code,200)
        self.student.refresh_from_db()
        self.assertTrue(self.student.check_password(self.new_password))
        self.assertNotIn('password',r.data)
    def test_crud_and_no_password_in_responses(self):
        self.login(self.admin)
        r=self.client.post('/api/v1/users/',{'username':'nuevo','email':'nuevo@campus.test','matricula':'UT002','password':self.new_password})
        self.assertEqual(r.status_code,201)
        self.assertNotIn('password',r.data)
        pk=r.data['id']
        self.assertTrue(User.objects.get(pk=pk).check_password(self.new_password))
        for url in ['/api/v1/users/',f'/api/v1/users/{pk}/']:
            r=self.client.get(url)
            self.assertEqual(r.status_code,200)
            for item in r.data if isinstance(r.data,list) else [r.data]:
                self.assertNotIn('password',item)
        self.assertEqual(self.client.delete(f'/api/v1/users/{pk}/').status_code,204)
    def test_schema_documents_matricula_and_password_write_only(self):
        r=self.client.get('/swagger.json')
        self.assertEqual(r.status_code,200)
        schema=r.data
        user=schema['definitions']['User']
        self.assertIn('matricula',user['properties'])
        self.assertNotIn('password',schema['definitions']['PublicUser']['properties'])
        self.assertTrue(__import__('users.serializers',fromlist=['UserSerializer']).UserSerializer().fields['password'].write_only)
