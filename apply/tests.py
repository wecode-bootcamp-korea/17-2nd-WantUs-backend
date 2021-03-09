import jwt
import bcrypt
import json

from django.test        import TestCase, Client

from my_settings    import SECRET_KEY, ALGORITHM
from user.models    import User, WorkExperience
from posting.models import (
        Posting,
        Occupation,
        Company,
        CompanyImage,
        CompanyDetail,
        State,
        County,
        Like,
        JobCategory,
        BookMark,
        TagDetail,
        Tag,
        CompanyTag
    )
from apply.models   import (
    Apply,
    ProcessStatus,
    RewardStatus
)

client = Client()

class ApplyViewTest(TestCase):
    def setUp(self):
        User.objects.create(
            id        = 1,
            name      = '로그인',
            email     = 'wecode_signin@naver.com',
            image_url = 'https://wecode.co.kr/static/media/song.2cfd0cb6.png'
        )
        tag1 = Tag.objects.create(
            id   = 1,
            name = '연봉수준'
        )

        tag_detail1 = TagDetail.objects.create(
            id   = 1,
            name = '#연봉업계평균이상',
            tag  = tag1
        )

        company1 = Company.objects.create(
            name        = '멋쟁이은우처럼',
            icon        = '123',
            description = '~.~'
        )

        state1 = State.objects.create(
            id   = 1,
            name = '서울'
        )

        county1 = County.objects.create(
            id   = 1,
            name = '종로'
        )

        company_detail1 = CompanyDetail.objects.create(
            company   = company1,
            name      = '본사',
            address   = '서울시',
            latitude  = 12.34,
            longitude = 12.34,
            state     = state1,
            county    = county1
        )

        company_tag1 = CompanyTag.objects.create(
            company    = company1,
            tag_detail = tag_detail1
        )

        occupation1 = Occupation.objects.create(
            name = '개발'
        )
        
        job_category1 = JobCategory.objects.create(
            id         = 1,
            name       = '파이썬 개발자',
            occupation = occupation1
        )

        work_experience1 = WorkExperience.objects.create(
            name = '신입'
        )

        Posting.objects.create(
            id              = 1,
            title           = '모집합니다1',
            job_category    = job_category1,
            company_detail  = company_detail1,
            reward          = 1,
            description     = 'asd',
            end_date        = '2021-03-05',
            work_experience = work_experience1
        )

        ProcessStatus.objects.create(
            id   = 1,
            name = '지원완료'
        )

        RewardStatus.objects.create(
            id   = 1,
            name = '신청'
        )

    def tearDown(self):
        Tag.objects.all().delete
        TagDetail.objects.all().delete
        Company.objects.all().delete
        State.objects.all().delete
        County.objects.all().delete
        CompanyDetail.objects.all().delete
        CompanyTag.objects.all().delete
        JobCategory.objects.all().delete
        WorkExperience.objects.all().delete
        Posting.objects.all().delete
        User.objects.all().delete
        ProcessStatus.objects.all().delete
        RewardStatus.objects.all().delete

    def test_apply_post_pass(self):
        data = {'posting':1}

        token    = jwt.encode({'id': User.objects.get(id=1).id}, SECRET_KEY, algorithm=ALGORITHM)
        headers  = {'HTTP_AUTHORIZATION': token}
        response = client.post('/apply', json.dumps(data), content_type='application/json', **headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'SUCCESS'})

    def test_apply_post_faild(self):
        data = {'aaa':1}

        token    = jwt.encode({'id': User.objects.get(id=1).id}, SECRET_KEY, algorithm=ALGORITHM)
        headers  = {'HTTP_AUTHORIZATION': token}
        response = client.post('/apply', json.dumps(data), content_type='application/json', **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'KEY_ERROR'})