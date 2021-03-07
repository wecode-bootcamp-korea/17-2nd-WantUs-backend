import jwt
import boto3
import mock

from django.core.files import File
from django.test       import TestCase, Client
from unittest.mock     import patch, MagicMock

from my_settings       import ALGORITHM, SECRET_KEY, S3KEY, S3SECRETKEY
from user.models       import User
from resume.models     import ResumeFile, ResumeStatus

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
        file = mock.MagicMock(spec=File, name='file.pdf')
        file.name = 'file.pdf'
        class MockedResponse:
            def json(self):
                return None
        mock_s3_client.upload_fileobj = MagicMock(return_value=MockedResponse())
        user   = User.objects.get(id=1)
        token  = jwt.encode({'id': user.id}, SECRET_KEY, algorithm=ALGORITHM)
        client = Client()
        data = {'resume': file}
        response = client.post('/resume/upload', data, **{'HTTP_Authorization': token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'SUCCESS', 'data': ResumeFile.objects.get(user=user).file_url})
    
    @patch('resume.views.boto3')
    def test_post_unallowedfile(self, mock_s3_client):
        file = mock.MagicMock(spec=File, name='file.txt')
        file.name = 'file.txt'
        class MockedResponse:
            def json(self):
                return None
        mock_s3_client.upload_fileobj = MagicMock(return_value=MockedResponse())
        user   = User.objects.get(id=1)
        token  = jwt.encode({'id': user.id}, SECRET_KEY, algorithm=ALGORITHM)
        client = Client()
        data = {'resume': file}
        response = client.post('/resume/upload', data, **{'HTTP_Authorization': token})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'PLEASE_UPLOAD_PDF'})

    def test_post_nofile(self):
        user   = User.objects.get(id=1)
        token  = jwt.encode({'id': user.id}, SECRET_KEY, algorithm=ALGORITHM)
        client = Client()
        response = client.post('/resume/upload', **{'HTTP_Authorization': token})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'FILE_DOES_NOT_EXIST'})
