import jwt
import bcrypt
import json

from django.test import TestCase, Client
from django.http    import JsonResponse

from unittest.mock  import patch, MagicMock
from my_settings    import SECRET_KEY, ALGORITHM
from user.models    import User
from .models        import (
        Resume,
        Education,
        Language,
        Career
        )

client = Client()
class ResumeMainTest(TestCase):
    def setUp(self):
        user    = User.objects.create(name='도나쓰', email='dd@g.com')
        resume  = Resume.objects.create(user=user, title=f'{user.name}의 이력서'+str(Resume.objects.filter(user=user).count()+1))
        resume  = Resume.objects.create(user=user, title=f'{user.name}의 이력서'+str(Resume.objects.filter(user=user).count()+1))

    def tearDown(self):
        User.objects.all().delete
        Resume.objects.all().delete()

    def test_resume_main_get_sucess(self):
        user_id     = User.objects.get(name='도나쓰').id
        token       = jwt.encode({'id' : user_id}, SECRET_KEY, algorithm=ALGORITHM)
        headers     = {'HTTP_Authorization' : token}
        response    = client.get('/cv/list', **headers, content_type='application/json')
        
        self.assertEqual(status_code, 200)

    def test_resume_main_post_sucess(self):
        user       = User.objects.get(name='도나쓰')
        token       = jwt.encode({'id' : user.id}, SECRET_KEY, algorithm=ALGORITHM)
        headers     = {'HTTP_Authorization' : token}
        response    = client.post('/cv/list', **headers, content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
