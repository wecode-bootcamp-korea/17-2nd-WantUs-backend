import jwt
import bcrypt
import json

from django.test        import TestCase, Client

from my_settings    import SECRET_KEY, ALGORITHM
from user.models    import User, WorkExperience
from .models        import (
        Apply,
        RewardStatus,
        ProcessStatus
)
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

class MyWantusTest(TestCase):
    maxDiff=None
    def setUp(self):
        User.objects.create(
                            id           = 1,
                            name         = "보라돌이",
                            email        = "purple@g.com",
                            phone_number = "010-1111-1111",
                            image_url    = "http://image"
                            )

        state = State.objects.create(name = '서울')

        c1 = County.objects.create(name = '강남구')
        c2 = County.objects.create(name = '강동구')

        Company.objects.create(
                            id          = 1,
                            name        = '윜코드',
                            icon        ='윜코드위고두',
                            description = '함께해서윜코드'
                                    )
        Company.objects.create(
                            id          = 2,
                            name        = '채현테크',
                            icon        = '대충엄청멋진아이콘',
                            description = '복지는없어요죄송해요'
                            )
        com_img1 = CompanyImage.objects.create(
                                            id          = 1,
                                            company_id  = 1,
                                            image_url   = 'http://image'
                                            )
        com_img2 = CompanyImage.objects.create(
                                            id          = 2,
                                            company_id  = 2,
                                            image_url   = 'http://image2'
                                            )
        CompanyDetail.objects.create(
                                    id          = 1,
                                    company_id  = 1,
                                    name        = '선릉2호점',
                                    address     = '테헤란로',
                                    latitude    = 123.123,
                                    longitude   = 321.321,
                                    state       = state,
                                    county      = c1
                                    )
        CompanyDetail.objects.create(
                                    id          = 2,
                                    company_id  = 2,
                                    name        = '우리집1호점',
                                    address     = '우리집주소',
                                    latitude    = 333.333,
                                    longitude   = 222.222,
                                    state       = state,
                                    county      = c2
                                    )

        occupation = Occupation.objects.create(name = '개발')

        JobCategory.objects.create(
                                id          = 1,
                                name        = '웹 개발자',
                                occupation  = occupation
                                )
        JobCategory.objects.create(
                                id          = 2,
                                name        = '앱 개발자',
                                occupation  = occupation
                                )

        WorkExperience.objects.create(
                                    id      = 1,
                                    name    = '신입'
                                    )
        WorkExperience.objects.create(
                                    id      = 2,
                                    name    = '1년차'
                                    )
        Tag.objects.create(
                        id   = 1,
                        name = '복지'
                        )

        TagDetail.objects.create(
                            id     = 1,
                            name   = '#스톡옵션',
                            tag_id = 1
                            )
        TagDetail.objects.create(
                            id     = 2,
                            name   = '#마사지기계',
                            tag_id = 1
                            )

        CompanyTag.objects.create(
                                id            = 1,
                                tag_detail_id = 1,
                                company_id    = 1
                                )
        CompanyTag.objects.create(
                                id            = 2,
                                tag_detail_id = 2,
                                company_id    = 1
                                )

        p1 = Posting.objects.create(
                                id                 = 1,
                                title              = '개발자구해요11',
                                job_category_id    = 1,
                                company_detail_id  = 1,
                                reward             = 10,
                                description        = '오면잘해줄께',
                                create_at          = '2020-10-10',
                                end_date           = '2021-04-03',
                                work_experience_id = 1
                                )

        p2 = Posting.objects.create(
                                id                 = 2,
                                title              = '개발자구해요22',
                                job_category_id    = 2,
                                company_detail_id  = 1,
                                reward             = 20,
                                description        = '대충구한다는말',
                                create_at          = '2020-05-05',
                                end_date           = '2021-04-03',
                                work_experience_id = 2
                                )

        p3 = Posting.objects.create(
                                id                 = 3,
                                title              = '개발자구해요33',
                                job_category_id    = 2,
                                company_detail_id  = 2,
                                reward             = 15,
                                description        = '오지마',
                                create_at          = '2020-08-07',
                                end_date           = '2021-04-03',
                                work_experience_id = 2
                                )
        p4 = Posting.objects.create(
                                id                 = 4,
                                title              = '개발자구해요44',
                                job_category_id    = 2,
                                company_detail_id  = 2,
                                reward             = 30,
                                description        = '정신차리는 회사',
                                create_at          = '2020-01-01',
                                end_date           = '2021-04-03',
                                work_experience_id = 1
                                )

        Like.objects.create(
                        id      = 1,
                        user_id = 1,
                        posting = p1
                        )
        Like.objects.create(
                        id      = 2,
                        user_id = 1,
                        posting = p2
                        )
        Like.objects.create(
                        id      = 3,
                        user_id = 1,
                        posting = p3
                        )
        Like.objects.create(
                        id      = 4,
                        user_id = 1,
                        posting = p4
                        )
        
        BookMark.objects.create(
                        user_id = 1,
                        posting = p1
                        )
        BookMark.objects.create(
                        user_id = 1,
                        posting = p2
                        )
        BookMark.objects.create(
                        user_id = 1,
                        posting = p3
                        )
        BookMark.objects.create(
                        user_id = 1,
                        posting = p4
                        )
        
        ProcessStatus.objects.create(
                                id   = 1,
                                name = '지원 완료'
                                )
        ProcessStatus.objects.create(
                                id   = 2,
                                name = '서류 통과'
                                )
        ProcessStatus.objects.create(
                                id   = 3,
                                name = '최종 합격'
                                )
        ProcessStatus.objects.create(
                                id   = 4,
                                name = '불합격'
                                )

        RewardStatus.objects.create(
                                id  = 1,
                                name = '신청 완료'
                                )
        RewardStatus.objects.create(
                                id  = 2,
                                name = '지급 완료'
                                )
        RewardStatus.objects.create(
                                id  = 3,
                                name = '반려'
                                )
        Apply.objects.create(
                        id                  = 1,
                        user_id             = 1,
                        posting_id          = 1,
                        process_status_id   = 1,
                        reward_status_id    = 1
                        )

        Apply.objects.create(
                        id                  = 2,
                        user_id             = 1,
                        posting_id          = 1,
                        process_status_id   = 2,
                        reward_status_id    = 1
                        )
        Apply.objects.create(
                        id                  = 3,
                        user_id             = 1,
                        posting_id          = 1,
                        process_status_id   = 3,
                        reward_status_id    = 2
                        )
        Apply.objects.create(
                        id                  = 4,
                        user_id             = 1,
                        posting_id          = 1,
                        process_status_id   = 4,
                        reward_status_id    = 3
                        )
    
    def tearDown(self):
        User.objects.all().delete()
        WorkExperience.objects.all().delete()
        Posting.objects.all().delete()
        Occupation.objects.all().delete()
        Company.objects.all().delete()
        CompanyImage.objects.all().delete()
        CompanyDetail.objects.all().delete()
        State.objects.all().delete()
        County.objects.all().delete()
        Like.objects.all().delete()
        JobCategory.objects.all().delete()
        BookMark.objects.all().delete()
        Apply.objects.all().delete()


    def test_mywantus_get_success(self):
        user = User.objects.get(id=1)
        token = jwt.encode({'id' : user.id}, SECRET_KEY, algorithm=ALGORITHM)

        response = client.get('/apply/mywanted', **{'HTTP_AUTHORIZATION' : token})
        self.assertEqual(response.json()['user'], {
                'profile'       : "http://image",
                'name'          : "보라돌이",
                'email'         : "purple@g.com",
                'phoneNumber'   : "010-1111-1111"
                })
        
        self.assertEqual(response.json()['apply'], {
                "stepFour"  : 1,
                "stepOne"   : 1,
                "stepThree" : 1,
                "stepTwo"   : 1
                })

        self.assertEqual(response.json()['book'], [
            {
                "id"            : 1,
                "category"      : "개발",
                "city"          : "서울",
                "company"       : "윜코드",
                "end"           : "2021-04-03",
                "image"         : "http://image",
                "state"         : "강남구",
                "subCategory"   : "웹 개발자",
                "tags"          : [
                                "#스톡옵션",
                                "#마사지기계"
                                ],
                "title"         : "개발자구해요11"
                },
            {
                "id"            : 2,
                "category"      : "개발",
                "city"          : "서울",
                "company"       : "윜코드",
                "end"           : "2021-04-03",
                "image"         : "http://image",
                "state"         : "강남구",
                "subCategory"   : "앱 개발자",
                "tags"          : [
                                "#스톡옵션",
                                "#마사지기계"
                                ],
                "title"         : "개발자구해요22"
                },
            {
                "id"            : 3,
                "category"      : "개발",
                "city"          : "서울",
                "company"       : "채현테크",
                "end"           : "2021-04-03",
                "image"         : "http://image2",
                "state"         : "강동구",
                "subCategory"   : "앱 개발자",
                "tags"          : [],
                "title"         : "개발자구해요33"
                },
            {
                "id"            : 4,
                "category"      : "개발",
                "city"          : "서울",
                "company"       : "채현테크",
                "end"           : "2021-04-03",
                "image"         : "http://image2",
                "state"         : "강동구",
                "subCategory"   : "앱 개발자",
                "tags"          : [],
                "title"         : "개발자구해요44"
            }])

        self.assertEqual(response.json()['like'], [
            {
                "id"            : 1,
                "city"          : "서울",
                "company"       : "윜코드",
                "image"         : "http://image",
                "state"         : "강남구",
                "title"         : "개발자구해요11"
                },
            {
                "id"            : 2,
                "city"          : "서울",
                "company"       : "윜코드",
                "image"         : "http://image",
                "state"         : "강남구",
                "title"         : "개발자구해요22"
                },
            {
                "id"            : 3,
                "city"          : "서울",
                "company"       : "채현테크",
                "image"         : "http://image2",
                "state"         : "강동구",
                "title"         : "개발자구해요33"
                },
            {
                "id"            : 4,
                "city"          : "서울",
                "company"       : "채현테크",
                "image"         : "http://image2",
                "state"         : "강동구",
                "title"         : "개발자구해요44"
                }])

        self.assertEqual(response.status_code, 200)
    
    def test_mywantus_does_not_exist(self):
        user = User.objects.get(id=1)
        token = jwt.encode({'id' : 4}, SECRET_KEY, algorithm=ALGORITHM)
        response = client.get('/apply/mywanted', **{'HTTP_AUTHORIZATION' : token})

        self.assertEqual(response.json()['message'], 'DOES_NOT_EXIST')
    
    def test_mywantus_does_invalid_token(self):
        user = User.objects.get(id=1)
        token = jwt.encode({'id' : 1}, SECRET_KEY, algorithm=ALGORITHM)
        response = client.get('/apply/mywanted', **{'HTTP_AUTHORIZATION' : '가짜토큰'})

        self.assertEqual(response.json()['message'], 'INVALID_TOKEN')
