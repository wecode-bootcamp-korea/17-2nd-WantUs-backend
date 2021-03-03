import json
import bcrypt
import jwt

from django.test    import (
    TestCase,
    Client
)
from unittest.mock  import (
    patch, 
    MagicMock
)

from user.models import User
from posting.models import JobCategory, Occupation
from utils       import SECRET_KEY, ALGORITHM

client = Client()

class SignUpTest(TestCase):
    def setUp(self):
        bytes_pw  = bytes('12345678', 'utf-8')
        hashed_pw = bcrypt.hashpw(bytes_pw, bcrypt.gensalt())

        User.objects.create(
            name      = '로그인',
            email     = 'wecode_signin@naver.com',
            image_url = 'https://wecode.co.kr/static/media/song.2cfd0cb6.png'
        )

    def tearDown(self):
        User.objects.filter(name='로그인').delete()
    
    @patch('user.views.requests')
    def test_signup_get_pass(self, mock_request):

        class MockedResponse:
            def json(self):
                return {
                    'id' : 1234,
                    'kakao_account': {
                        'profile' : {
                            'nickname': '회원가입',
                        },
                        'email' : 'wecode_signup@naver.com',
                    },
                }
            
        mock_request.request = MagicMock(return_value = MockedResponse())
        headers  = {'HTTP_AUTHORIZATION': '1234'}
        response = client.get('/user/sign', content_type='applications/json', **headers)

        user_id = jwt.decode(response.json()['accessToken'], SECRET_KEY, ALGORITHM)['id']

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {
            'message': 'SUCCESS', 
            'accessToken': jwt.encode({'id': user_id}, SECRET_KEY, algorithm=ALGORITHM)
        })
    
    @patch('user.views.requests')
    def test_signin_get_pass(self, mock_request):
        
        class MockedResponse:
            def json(self):
                return {
                    'id' : 1234,
                    'kakao_account': {
                        'profile' : {
                            'nickname': '로그인',
                        },
                        'email' : 'wecode_signin@naver.com',
                    },
                }
            
        mock_request.request = MagicMock(return_value = MockedResponse())
        headers  = {'HTTP_AUTHORIZATION': '1234'}
        response = client.get('/user/sign', content_type='applications/json', **headers)

        user_id = jwt.decode(response.json()['accessToken'], SECRET_KEY, ALGORITHM)['id']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'message': 'SUCCESS', 
            'accessToken': jwt.encode({'id': user_id}, SECRET_KEY, algorithm=ALGORITHM)
        })

    @patch('user.views.requests')
    def test_signup_get_key_error(self, mock_request):
        
        class MockedResponse:
            def json(self):
                return {
                    'id' : 1234,
                    'kakao_account': {
                        'profile' : {
                            'nickname': '로그인',
                            'email' : 'wecode_signin@naver.com',
                        },
                    },
                }
            
        mock_request.request = MagicMock(return_value = MockedResponse())
        headers  = {'HTTP_AUTHORIZATION': '1234'}
        response = client.get('/user/sign', content_type='applications/json', **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'KEY_ERROR'})

class ProfileTest(TestCase):
    def setUp(self):
        user = User.objects.create(
            name  = '위코더',
            email = 'wecode@test.com'
        )
        occu = Occupation.objects.create(name = '코딩')
        job = JobCategory.objects.create(
            name = '은우사랑모임',
            occupation = occu
        )
        user.job_category.add(job)
    
    def tearDown(self):
        user = User.objects.get(name='위코더')
        user.job_category.all().delete
        Occupation.objects.filter(name='코딩').delete
        user.delete

    def test_profile_patch_pass(self):
        user  = User.objects.get(name='위코더')
        token = jwt.encode({'id':user.id}, SECRET_KEY, algorithm=ALGORITHM)
        data  = {'phoneNumber':'010-1234-1234'}

        headers  = {'HTTP_AUTHORIZATION': token}
        response = client.patch('/user/profile', json.dumps(data), content_type='applications/json', **headers)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(),{'message': 'SUCCESS'})

    def test_profile_patch_have_not_data(self):
        user  = User.objects.get(name='위코더')
        token = jwt.encode({'id':user.id}, SECRET_KEY, algorithm=ALGORITHM)

        headers  = {'HTTP_AUTHORIZATION': token}
        response = client.patch('/user/profile', content_type='applications/json', **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{'message': 'JSON_DECODE_ERROR'})

    def test_profile_get_have_not_token(self):
        headers  = {'HTTP_AUTHORIZATION': ''}
        response = client.patch('/user/profile', content_type='applications/json', **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'INVALID_TOKEN'})
