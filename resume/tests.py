import jwt
import json
import boto3
import mock
import json

from django.core.files  import File
from django.test        import TestCase, Client
from unittest.mock      import patch, MagicMock
from django.http        import JsonResponse

from resume.models      import (
        ResumeFile,
        Resume,
        ResumeStatus,
        Education,
        Language,
        Career
        )
from my_settings        import ALGORITHM, SECRET_KEY, S3KEY, S3SECRETKEY
from user.models        import User

client   = Client()

class ResumeFileUploadViewTest(TestCase):
    def setUp(self):
        User.objects.create(id=1, name='gildong', email='cat@cat')
        ResumeStatus.objects.create(id=3, status_code='ddd')

    def tearDown(self):
        ResumeFile.objects.all().delete()
        ResumeStatus.objects.all().delete()
        User.objects.filter(id=1).delete()

    @patch('resume.views.boto3')
    def test_post_success(self, mock_s3_client):
        file      = mock.MagicMock(spec=File, name='file.pdf')
        file.name = 'file.pdf'
        class MockedResponse:
            def json(self):
                return None
        mock_s3_client.upload_fileobj = MagicMock(return_value=MockedResponse())
        user                          = User.objects.get(id=1)
        token                         = jwt.encode({'id': user.id}, SECRET_KEY, algorithm=ALGORITHM)
        client                        = Client()
        data                          = {'resume': file}
        response                      = client.post('/resume/upload', data, **{'HTTP_Authorization': token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'SUCCESS', 'data': ResumeFile.objects.get(user=user).file_url})

    @patch('resume.views.boto3')
    def test_post_unallowedfile(self, mock_s3_client):
        file      = mock.MagicMock(spec=File, name='file.txt')
        file.name = 'file.txt'
        class MockedResponse:
            def json(self):
                return None
        mock_s3_client.upload_fileobj = MagicMock(return_value=MockedResponse())
        user                          = User.objects.get(id=1)
        token                         = jwt.encode({'id': user.id}, SECRET_KEY, algorithm=ALGORITHM)
        client                        = Client()
        data                          = {'resume': file}
        response                      = client.post('/resume/upload', data, **{'HTTP_Authorization': token})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'PLEASE_UPLOAD_PDF'})


    def test_post_nofile(self):
        user     = User.objects.get(id=1)
        token    = jwt.encode({'id': user.id}, SECRET_KEY, algorithm=ALGORITHM)
        client   = Client()
        response = client.post('/resume/upload', **{'HTTP_Authorization': token})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'FILE_DOES_NOT_EXIST'})

class ResumePartialTest(TestCase):
    def setUp(self):
        User.objects.create(
                        id           = 1, 
                        name         = '도나쓰', 
                        email        = 'c_hyun403@gmail.com', 
                        phone_number = '010-1111-1111'
                        )
        User.objects.create(
                        id           = 2, 
                        name         = '밀쉐', 
                        email        = 'milk@gmail.com', 
                        phone_number = '010-1111-2222'
                        )
        ResumeStatus.objects.create(
                                id          = 1, 
                                status_code = '작성중'
                        )
        Resume.objects.create(
                            id        = 1,
                            user_id   = 1, 
                            title     = 'test이력서', 
                            introduce = '테스트자기소개'
                                )
        Resume.objects.create(
                            id        = 2,
                            user_id   = 2, 
                            title     = 'test이력서222', 
                            introduce = '테스트자기소개'
                                )
        Career.objects.create(
                            id  = 1, 
                            resume_id  = 1, 
                            name       = '회사', 
                            start_date = '1995-04-03', 
                            end_date   = '2020-04-03'
                            )
        Language.objects.create(
                            id         = 1,
                            resume_id  = 1, 
                            name       = '일본어', 
                            start_date = '1995-04-03', 
                            end_date   = '2020-04-03'
                            )
        Education.objects.create(
                            id         = 1, 
                            resume_id  = 1, 
                            start_date = '2000-04-03', 
                            end_date   = '2020-04-03', 
                            name       = '학교'
                            )
        Education.objects.create(
                            id         = 2, 
                            resume_id  = 1, 
                            start_date = '2000-04-03', 
                            name       = '교육원'
                            )
    
    def tearDown(self):
        User.objects.all().delete()
        Resume.objects.all().delete()
        Career.objects.all().delete()
        Language.objects.all().delete()
        Education.objects.all().delete()

    def test_resume_partial_get_sucess(self):
        user     = User.objects.get(id=1)
        token    = jwt.encode({'id':user.id}, SECRET_KEY, algorithm=ALGORITHM)
        headers  = {'HTTP_AUTHORIZATION' : token}
        resume   = Resume.objects.get(title='test이력서')
        response = client.get('/resume/1', content_type='application/json', **headers)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['result'], {
            'userInfo'  : {
                'name'        : '도나쓰',
                'email'       : 'c_hyun403@gmail.com',
                'phoneNumber' : '010-1111-1111'
                },
            'resumeIntro' : '테스트자기소개',
            'resumeTitle' : 'test이력서',
            'career' : [{
                'id'    : 1,
                'Name'  : '회사',
                'Start' : '1995-04-03',
                'End'   : '2020-04-03'
                }],
            'education' : [
                {
                    'id'    : 1,
                    'Name'  : '학교',
                    'Start' : '2000-04-03',
                    'End'   : '2020-04-03'
                    },
                {
                    'id'    : 2,
                    'Name'  : '교육원',
                    'Start' : '2000-04-03',
                    'End'   : None
                    }
                ],
            'language' : [{
                'id'    : 1,
                'Name'  : '일본어',
                'Start' : '1995-04-03',
                'End'   : '2020-04-03'
                }],
            })
    
    def test_resume_partial_get_invalide_user(self):
        user     = User.objects.get(id=1)
        token    = jwt.encode({'id': user.id}, SECRET_KEY, algorithm=ALGORITHM)
        headers  = {'HTTP_AUTHORIZATION' : token}
        resume   = Resume.objects.get(title='test이력서')
        response = client.get('/resume/2', content_type='application/json', **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['message'], 'INVALID_USER')
        
    def test_resume_partial_get_invalide_resume(self):
        user     = User.objects.get(id=1)
        token    = jwt.encode({'id':user.id}, SECRET_KEY, algorithm=ALGORITHM)
        headers  = {'HTTP_AUTHORIZATION' : token}
        resume   = Resume.objects.get(title='test이력서')
        response = client.get('/resume/100', content_type='application/json', **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['message'], 'INVALID_RESUME')

    def test_resume_delete_success(self):
        user        = User.objects.get(id=1)
        token       = jwt.encode({'id' : user.id}, SECRET_KEY, algorithm=ALGORITHM)
        headers     = {'HTTP_AUTHORIZATION' : token}
        response    = client.delete('/resume/1', content_type='application/json', **headers)

        self.assertEqual(response.json()['message'], 'SUCCESS')
        self.assertEqual(response.status_code, 200)

    def test_resume_delete_invalid_user(self):
        user        = User.objects.get(id=2)
        token       = jwt.encode({'id' : user.id}, SECRET_KEY, algorithm=ALGORITHM)
        headers     = {'HTTP_AUTHORIZATION' : token}
        response    = client.delete('/resume/1', content_type='application/json', **headers)

        self.assertEqual(response.json()['message'], 'INVALID_USER')
        self.assertEqual(response.status_code, 400)

    def test_resume_delete_invalid_resume(self):
        user        = User.objects.get(id=2)
        token       = jwt.encode({'id' : user.id}, SECRET_KEY, algorithm=ALGORITHM)
        headers     = {'HTTP_AUTHORIZATION' : token}
        response    = client.delete('/resume/10', content_type='application/json', **headers)

        self.assertEqual(response.json()['message'], 'INVALID_RESUME')
        self.assertEqual(response.status_code, 400)

class ResumeTest(TestCase):
    maxDiff=None
    def setUp(self):
        User.objects.create(
                            id      = 1,
                            name    = '보라돌이',
                            email   = 'purple@g.com'
                            )
        User.objects.create(
                            id      = 2,
                            name    = '뚜비',
                            email   = 'green@g.com'
                            )
        
        ResumeStatus.objects.create(
                                    id          = 1,
                                    status_code = '작성중'
                                    )
        ResumeStatus.objects.create(
                                    id          = 2,
                                    status_code = '작성완료'
                                    )
        ResumeStatus.objects.create(
                                    id          = 3,
                                    status_code = '첨부파일'
                                    )


        Resume.objects.create(
                            id          = 1,
                            user_id     = 1,
                            title       = '보라돌이의 이력서1',
                            )
        Resume.objects.create(
                            id          = 3,
                            user_id     = 2,
                            title       = '뚜비의 이력서1',
                            )
        ResumeFile.objects.create(
                            id          = 2,
                            user_id     = 1,
                            title       = '보라돌이의 업로드 이력서1',
                            file_url    = 'file의 url',
                            uuidcode     = 'uuu'
                            )
        Resume.objects.create(
                            id          = 4,
                            user_id     = 1,
                            title       = '보라돌이의 이력서2',
                            )
    def tearDown(self):
        User.objects.all().delete()
        Resume.objects.all().delete()
        ResumeFile.objects.all().delete()

    def test_resume_get_success(self):
        user        = User.objects.get(id=1)
        token       = jwt.encode({'id' : user.id}, SECRET_KEY, algorithm=ALGORITHM)
        headers     = {'HTTP_AUTHORIZATION' : token}
        response    = client.get('/resume', content_type='application/json', **headers)

        resumes     = Resume.objects.filter(user=user)
        self.assertEqual(response.json()['result'], [
            {
                'id'        : 1, 
                'name'      : '보라돌이의 이력서1', 
                'date'      : '2021-03-11', 
                'status'    : '작성중', 
                'matchUp'   : False
                }, 
            {
                'id'        : 2, 
                'name'      : '보라돌이의 업로드 이력서1', 
                'date'      : '2021-03-11', 
                'status'    : '첨부파일', 
                'matchUp'   : False
                },
            {
                'id'        : 4, 
                'name'      : '보라돌이의 이력서2', 
                'date'      : '2021-03-11', 
                'status'    : '작성중', 
                'matchUp'   : False
                }])
        self.assertEqual(response.status_code, 200)

    def test_resume_post_success(self):
        user        = User.objects.get(id=1)
        token       = jwt.encode({'id' : user.id}, SECRET_KEY, algorithm=ALGORITHM)
        headers     = {'HTTP_AUTHORIZATION' : token}
        response    = client.post('/resume', content_type='application/json', **headers)
        
        self.assertEqual(response.json()['result'], 5)
        self.assertEqual(response.status_code, 201)

class ResumeFileDeleteViewTest(TestCase):
    def setUp(self):
        User.objects.create(id=1, name='gildong', email='cat@cat')
        ResumeStatus.objects.create(id=3, status_code='ddd')
        ResumeFile.objects.create(id=1, user=User.objects.get(id=1), title='aaa', file_url='aaaa', uuidcode='ased', complete_status=ResumeStatus.objects.get(id=3))

    def tearDown(self):
        ResumeFile.objects.all().delete()
        ResumeStatus.objects.all().delete()
        User.objects.filter(id=1).delete()
    
    @patch('resume.views.urllib.request')
    @patch('resume.views.boto3')
    def test_delete(self, mock_s3_client, mock_urllib):
        class MockedResponse:
            def json(self):
                return None

        user      = User.objects.get(id=1)
        token     = jwt.encode({'id': user.id}, SECRET_KEY, algorithm=ALGORITHM)
        client    = Client()
        resume_id = ResumeFile.objects.get(user=user).id

        mock_urllib.request           = MagicMock(return_value=MockedResponse())
        mock_s3_client.delete_objects = MagicMock(return_value=MockedResponse())

        response  = client.delete(f"/resume/upload/{resume_id}", **{'HTTP_Authorization': token})
        
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json(), {'message': 'SUCCESS'})
    
    @patch('resume.views.boto3')
    def test_delete_fail(self, mock_s3_client):

        class MockedResponse:
            def json(self):
                return None

        user                          = User.objects.get(id=1)
        token                         = jwt.encode({'id': user.id}, SECRET_KEY, algorithm=ALGORITHM)
        client                        = Client()
        resume_id                     = ResumeFile.objects.get(user=user).id
        
        ResumeFile.objects.filter(user=user).update(file_url='https://wantusfile.s3.ap-northeast-2.amazonaws.com/aaa')
        
        mock_s3_client.delete_objects = MagicMock(return_value=MockedResponse())
        
        response                      = client.delete(f"/resume/upload/{resume_id}", **{'HTTP_Authorization': token})
        
        self.assertEquals(response.status_code, 404)
        self.assertEquals(response.json(), {'message': 'INVALID_URL'})
