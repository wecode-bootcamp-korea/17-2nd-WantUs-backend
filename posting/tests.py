import jwt
import bcrypt

from datetime           import date
from django.test        import TestCase, Client
from django.db.models   import Count

from unittest.mock  import patch, MagicMock
from my_settings    import SECRET_KEY, ALGORITHM
from user.models    import User, WorkExperience
from resume.models  import Resume, ResumeFile, ResumeStatus
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

class PostingDetailViewTest(TestCase):
    maxDiff = None
    def setUp(self):
        User.objects.create(
                            id    = 1, 
                            name  = 'gildong', 
                            email = 'cat@cat'
                            )
        Occupation.objects.create(
                                  id   = 1, 
                                  name = 'aaa'
                                  )
        WorkExperience.objects.create(
                                      id   = 1, 
                                      name = 'www'
                                      )
        ResumeStatus.objects.create(id          = 1,
                                    status_code = '작성중'
                                    )
        ResumeStatus.objects.create(id          = 2,
                                    status_code = '작성완료'
                                    )
        ResumeStatus.objects.create(id          = 3,
                                    status_code = '첨부파일'
                                    )
        ResumeFile.objects.create(id=1,
                                  user=User.objects.get(id=1),
                                  file_url='adsde',
                                  title='bbb',
                                  uuidcode='asdee',
                                  complete_status=ResumeStatus.objects.get(id=3)
                                  )
        Resume.objects.create(id=1,
                              user=User.objects.get(id=1),
                              is_default=False,
                              title='aaaa',
                              complete_status=ResumeStatus.objects.get(id=1),
                              introduce='bbb'
                              )
        Resume.objects.create(id=2,
                              user=User.objects.get(id=1),
                              is_default=True,
                              title='aaaa',
                              complete_status=ResumeStatus.objects.get(id=2),
                              introduce='bbb'
                              )
        Tag.objects.create(
                          id   = 1, 
                          name = 'gg'
                          )
        TagDetail.objects.create(
                                id   = 1, 
                                tag  = Tag.objects.get(id=1), 
                                name = 'ppp'
                                )
        TagDetail.objects.create(
                                id   = 2, 
                                tag  = Tag.objects.get(id=1), 
                                name = 'ppp'
                                )
        JobCategory.objects.create(
                                  id         = 1, 
                                  occupation = Occupation.objects.get(id=1), 
                                  name       = 'aaa'
                                  )
        State.objects.create(
                            id   = 1, 
                            name = 'aaa'
                            )
        County.objects.create(
                              id   = 1, 
                              name = 'aaaa')
        Company.objects.create(
                              id          = 1, 
                              name        = 'aaa', 
                              icon        = 'asesd', 
                              description = 'dases'
                              )
        Company.objects.create(
                               id          = 2, 
                               name        = 'bbb', 
                               icon        = 'asesd', 
                               description = 'dases'
                               )
        CompanyImage.objects.create(
                                    id        = 1, 
                                    company   = Company.objects.get(id=1), 
                                    image_url = 'asdefafasd')
        CompanyImage.objects.create(
                                    id        = 2, 
                                    company   = Company.objects.get(id=2), 
                                    image_url = 'asdefafasd')
        CompanyDetail.objects.create(
                                    id        = 1, 
                                    company   = Company.objects.get(id=1), 
                                    name      = 'ijonkm', 
                                    address   = 'asdqwndinm', 
                                    latitude  = 34, 
                                    longitude = 56, 
                                    state     = State.objects.get(id=1), 
                                    county    = County.objects.get(id=1)
                                    )
        CompanyDetail.objects.create(
                                    id        = 2, 
                                    company   = Company.objects.get(id=2), 
                                    name      = 'ijonkm', 
                                    address   = 'asdqwndinm', 
                                    latitude  = 34, 
                                    longitude = 56, 
                                    state     = State.objects.get(id=1), 
                                    county    = County.objects.get(id=1)
                                    )
        Posting.objects.create(
                              id              = 1, 
                              work_experience = WorkExperience.objects.get(id=1), 
                              title           = 'adnowpmpqwm', 
                              job_category    = JobCategory.objects.get(id=1), 
                              company_detail  = CompanyDetail.objects.get(id=1), 
                              reward          = 100, 
                              description     = 'asdeegmin', 
                              end_date        = '2021-04-03'
                              )
        Posting.objects.create(
                              id              = 2, 
                              work_experience = WorkExperience.objects.get(id=1), 
                              title           = 'adnowpmpqwm', 
                              job_category    = JobCategory.objects.get(id=1), 
                              company_detail  = CompanyDetail.objects.get(id=2), 
                              reward          = 100, 
                              description     = 'asdeegmin', 
                              end_date        = '2021-04-03'
                              )
        Like.objects.create(
                            id      = 1, 
                            user    = User.objects.get(id=1), 
                            posting = Posting.objects.get(id=1)
                            )
        CompanyTag.objects.create(
                                  id         = 1, 
                                  company    = Company.objects.get(id=1), 
                                  tag_detail = TagDetail.objects.get(id=1)
                                  )
        CompanyTag.objects.create(
                                  id         = 2, 
                                  company    = Company.objects.get(id=1), 
                                  tag_detail = TagDetail.objects.get(id=2)
                                  )
        BookMark.objects.create(
                               id      = 1, 
                               user    = User.objects.get(id=1), 
                               posting = Posting.objects.get(id=1)
                               )

    def tearDown(self):
        BookMark.objects.all().delete()
        Like.objects.all().delete()
        Resume.objects.all().delete()
        ResumeFile.objects.all().delete()
        ResumeStatus.objects.all().delete()
        User.objects.all().delete()
        CompanyTag.objects.all().delete()
        Occupation.objects.all().delete()
        WorkExperience.objects.all().delete()
        Tag.objects.all().delete()
        TagDetail.objects.all().delete()
        JobCategory.objects.all().delete()
        State.objects.all().delete()
        County.objects.all().delete()
        Company.objects.all().delete()
        CompanyImage.objects.all().delete()
        CompanyDetail.objects.all().delete()
        Posting.objects.all().delete()
  

    def test_postingdetail_liked_get_success(self):
        client   = Client()
        token    = jwt.encode({'id': User.objects.get(id=1).id}, SECRET_KEY, algorithm=ALGORITHM)
        response = client.get('/posting/1', **{'HTTP_Authorization': token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'SUCCESS', 'data': [
            {
                'id'           : 1,
                'title'        : 'adnowpmpqwm',
                'company'      : 'aaa',
                'city'         : 'aaa',
                'district'     : 'aaaa',
                'detailAddress': 'asdqwndinm',
                'latitude'     : 34,
                'longitude'    : 56,
                'tags'         : ['ppp', 'ppp'],
                'description'  : 'asdeegmin',
                'image'        : 'asdefafasd',
                'bonus'        : 100,
                'like'         : 1,
                'deadline'     : '2021-04-03',
                'logoSrc'      : 'asesd',
                'category'     : 'aaa',
                'user'         : 'gildong',
                'userBookmark' : True,
                'userLike'     : True,
                'userPhone'    : None,
                'userEmail'    : 'cat@cat',
                'resume'       : [
                                    {
                                     'id'              : 1,
                                     'title'           : 'aaaa',
                                     'date'            : date.today().isoformat(),
                                     'complete_status' : '작성중',
                                     'matchUp'         : False,
                                     },
                                    {
                                     'id'              : 2,
                                     'title'           : 'aaaa',
                                     'date'            : date.today().isoformat(),
                                     'complete_status' : '작성완료',
                                     'matchUp'         : True,
                                     },
                                    {
                                     'id'              : 1,
                                     'title'           : 'bbb',
                                     'date'            : date.today().isoformat(),
                                     'complete_status' : '첨부파일',
                                     'matchUp'         : False,
                                     },
                                    ],
                }
                ]
            }
            )
    
    def test_postingdetail_nonliked_get_success(self):
        client   = Client()
        token    = jwt.encode({'id': User.objects.get(id=1).id}, SECRET_KEY, algorithm=ALGORITHM)
        response = client.get('/posting/2', **{'HTTP_Authorization': token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'SUCCESS', 'data': [
            {
                'id'           : 2,
                'title'        : 'adnowpmpqwm',
                'company'      : 'bbb',
                'city'         : 'aaa',
                'district'     : 'aaaa',
                'detailAddress': 'asdqwndinm',
                'latitude'     : 34.0,
                'longitude'    : 56.0,
                'tags'         : [],
                'description'  : 'asdeegmin',
                'image'        : 'asdefafasd',
                'bonus'        : 100,
                'like'         : 0,
                'deadline'     : '2021-04-03',
                'logoSrc'      : 'asesd',
                'category'     : 'aaa',
                'user'         : 'gildong',
                'userLike'     : False,
                'userBookmark' : False,
                'userPhone'    : None,
                'userEmail'    : 'cat@cat',
                'resume'       : [
                                    {
                                     'id'              : 1,
                                     'title'           : 'aaaa',
                                     'date'            : date.today().isoformat(),
                                     'complete_status' : '작성중',
                                     'matchUp'         : False,
                                     },
                                    {
                                     'id'              : 2,
                                     'title'           : 'aaaa',
                                     'date'            : date.today().isoformat(),
                                     'complete_status' : '작성완료',
                                     'matchUp'         : True,
                                     },
                                    {
                                     'id'              : 1,
                                     'title'           : 'bbb',
                                     'date'            : date.today().isoformat(),
                                     'complete_status' : '첨부파일',
                                     'matchUp'         : False,
                                     },
                                    ],
                }
                ]
            }
            )
    
    def test_postingdetail_nonuser_get_success(self):
        client   = Client()
        response = client.get('/posting/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'SUCCESS', 'data': [
            {
                'id'           : 1,
                'title'        : 'adnowpmpqwm',
                'company'      : 'aaa',
                'city'         : 'aaa',
                'district'     : 'aaaa',
                'detailAddress': 'asdqwndinm',
                'latitude'     : 34,
                'longitude'    : 56,
                'tags'         : ['ppp', 'ppp'],
                'description'  : 'asdeegmin',
                'image'        : 'asdefafasd',
                'bonus'        : 100,
                'like'         : 1,
                'deadline'     : '2021-04-03',
                'logoSrc'      : 'asesd',
                'category'     : 'aaa',
                'user'         : None,
                'userLike'     : False,
                'userBookmark' : False
                        }
            ]
            }
            )

    def test_postingdetail_get_fail(self):
        client   = Client()
        response = client.get('/posting/100')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'message': 'BAD_REQUEST'})

class MainViewTest(TestCase):
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
        User.objects.create(
                            id      = 3,
                            name    = '나나',
                            email   = 'yellow@g.com'
                            )
        User.objects.create(
                            id      = 4,
                            name    = '뽀',
                            email   = 'red@g.com')

        state = State.objects.create(name = '서울')
        
        c1 = County.objects.create(name = '강남구')
        c2 = County.objects.create(name = '강동구')
        c3 = County.objects.create(name = '강북구')
        
        com1 = Company.objects.create(
                                    name        = '윜코드',
                                    icon        ='윜코드위고두',
                                    description = '함께해서윜코드'
                                    )
        com2 = Company.objects.create(
                                    name        = '불리자두', 
                                    icon        = '대충소용돌이', 
                                    description = '망겜아망하지마'
                                    )
        com3 = Company.objects.create(
                                    name        = '채현테크', 
                                    icon        = '대충엄청멋진아이콘', 
                                    description = '복지는없어요죄송해요'
                                    )
        com_img1 = CompanyImage.objects.create(
                                            id          = 1,
                                            company     = com3,
                                            image_url   = 'http://image'
                                            )
        com_img2 = CompanyImage.objects.create(
                                            id          = 2,
                                            company     = com3,
                                            image_url   = 'http://image2'
                                            )
        com_de1 = CompanyDetail.objects.create(
                                            id          = 1, 
                                            company     = com1, 
                                            name        = '선릉2호점',
                                            address     = '테헤란로',
                                            latitude    = 123.123, 
                                            longitude   = 321.321, 
                                            state       = state, 
                                            county      = c1
                                            )
        com_de2 = CompanyDetail.objects.create(
                                            id          = 2, 
                                            company     = com2, 
                                            name        = '우리집1호점', 
                                            address     = '우리집주소', 
                                            latitude    = 333.333, 
                                            longitude   = 222.222, 
                                            state       = state, 
                                            county      = c2
                                            )
        com_de3 = CompanyDetail.objects.create(
                                            id          = 3, 
                                            company     = com3, 
                                            name        = '거실1호점', 
                                            address     = '현관부터거실까지', 
                                            latitude    = 444.444, 
                                            longitude   = 555.555, 
                                            state       = state, 
                                            county      = c3
                                            )

        occupation = Occupation.objects.create(name = '개발자')

        job1 = JobCategory.objects.create(
                                        id          = 1, 
                                        name        = '웹개발자', 
                                        occupation  = occupation
                                        )
        job2 = JobCategory.objects.create(
                                        id          = 2, 
                                        name        = '앱개발자', 
                                        occupation  = occupation
                                        )
        job3 = JobCategory.objects.create(
                                        id          = 3, 
                                        name        = '개애발자', 
                                        occupation  = occupation
                                        )

        work1 = WorkExperience.objects.create(
                                            id      = 1, 
                                            name    = '신입'
                                            )
        work2 = WorkExperience.objects.create(
                                            id      = 2, 
                                            name    = '1년차'
                                            )
        work3 = WorkExperience.objects.create(
                                            id      = 3, 
                                            name    = '2년차'
                                            )


        p1 = Posting.objects.create(
                                id              = 1, 
                                title           = '개발자구해요11', 
                                job_category    = job1, 
                                company_detail  = com_de1, 
                                reward          = 10, 
                                description     = '오면잘해줄께', 
                                create_at       = '2020-10-10', 
                                end_date        = '2021-04-03', 
                                work_experience = work1
                                )
        
        p2 = Posting.objects.create(
                                id              = 2, 
                                title           = '개발자구해요22', 
                                job_category    = job2, 
                                company_detail  = com_de1, 
                                reward          = 20, 
                                description     = '대충구한다는말', 
                                create_at       = '2020-05-05', 
                                end_date        = '2021-04-03', 
                                work_experience = work3
                                )
        
        p3 = Posting.objects.create(
                                id              = 3, 
                                title           = '개발자구해요33', 
                                job_category    = job3, 
                                company_detail  = com_de2, 
                                reward          = 15, 
                                description     = '오지마', 
                                create_at       = '2020-08-07', 
                                end_date        = '2021-04-03', 
                                work_experience = work2
                                )
        p4 = Posting.objects.create(
                                id              = 4, 
                                title           = '개발자구해요44', 
                                job_category    = job3, 
                                company_detail  = com_de3, 
                                reward          = 30, 
                                description     = '정신차리는 회사', 
                                create_at       = '2020-01-01', 
                                end_date        = '2021-04-03', 
                                work_experience = work3
                                )

        Like.objects.create(
                        user_id = 1, 
                        posting = p1
                        )
        Like.objects.create(
                        user_id = 2, 
                        posting = p1
                        )
        Like.objects.create(
                        user_id = 1, 
                        posting = p2
                        )
        Like.objects.create(
                        user_id = 2, 
                        posting = p2
                        )
        Like.objects.create(
                        user_id = 3, 
                        posting = p2
                        )
        Like.objects.create(
                        user_id = 1, 
                        posting = p3
                        )
        Like.objects.create(
                        user_id = 1, 
                        posting = p4
                        )
        Like.objects.create(
                        user_id = 2, 
                        posting = p4
                        )
        Like.objects.create(
                        user_id = 3, 
                        posting = p4
                        )
        Like.objects.create(
                        user_id = 4, 
                        posting = p4
                        )

    def tearDown(self):
        User.objects.all().delete()
        WorkExperience.objects.all().delete()
        Posting.objects.all().delete(),
        Occupation.objects.all().delete(),
        Company.objects.all().delete(),
        CompanyImage.objects.all().delete(),
        CompanyDetail.objects.all().delete(),
        State.objects.all().delete(),
        County.objects.all().delete(),
        Like.objects.all().delete(),
        JobCategory.objects.all().delete()

    def test_posting_get_success(self):
        user                = User.objects.get(name='나나')
        token               = jwt.encode({'id' : user.id}, SECRET_KEY, algorithm=ALGORITHM)
        response            = client.get('/main', **{'HTTP_Authorization' : token})
        
        LIST_LIMIT_NUMBER   = 4
        set_postings1       = Posting.objects.annotate(like_num=Count('like')).all()
        
        like_postings       = set_postings1.order_by('-like_num')[:LIST_LIMIT_NUMBER]
        self.assertEqual(response.json()['likePosting'], [{
            "postingId" : 4,
            "imageUrl"  : 'http://image',
            "job"       : '개발자구해요44',
            "name"      : '채현테크',
            "city"      : '서울',
            "state"     : '강북구',
            "price"     : 30,
            "likeNum"   : 4
            },
            {
            "postingId" : 2,
            "imageUrl"  : None,
            "job"       : '개발자구해요22',
            "name"      : '윜코드',
            "city"      : '서울',
            "state"     : '강남구',
            "price"     : 20,
            "likeNum"   : 3
            },
            {
            "postingId" : 1,
            "imageUrl"  : None,
            "job"       : '개발자구해요11',
            "name"      : '윜코드',
            "city"      : '서울',
            "state"     : '강남구',
            "price"     : 10,
            "likeNum"   : 2
            },
            {
            "postingId" : 3,
            "imageUrl"  : None,
            "job"       : '개발자구해요33',
            "name"      : '불리자두',
            "city"      : '서울',
            "state"     : '강동구',
            "price"     : 15,
            "likeNum"   : 1
            }])
        
        self.assertEqual(response.json()['new'], [
            {
            "postingId" : 4,
            "imageUrl"  : 'http://image',
            "name"      : '채현테크',
            "job"       : '개발자',
            },
            {
            "postingId" : 3,
            "imageUrl"  : None,
            "name"      : '불리자두',
            "job"       : '개발자',
            },
            {
            "postingId" : 2,
            "imageUrl"  : None,
            "name"      : '윜코드',
            "job"       : '개발자',
            },
            {
            "postingId" : 1,
            "imageUrl"  : None,
            "name"      : '윜코드',
            "job"       : '개발자',
            }
            ])
        
        self.assertEqual(response.json()['thisWeek'], [
            {
            "imageUrl"  : 'http://image',
            "postingId" : 4,
            "job"       : '개발자구해요44',
            "name"      : '채현테크',
            "city"      : '서울',
            "state"     : '강북구',
            "price"     : 30,
            },
            {
            "imageUrl"  : None,
            "postingId" : 3,
            "job"       : '개발자구해요33',
            "name"      : '불리자두',
            "city"      : '서울',
            "state"     : '강동구',
            "price"     : 15,
            },
            {
            "imageUrl"  : None,
            "postingId" : 2,
            "job"       : '개발자구해요22',
            "name"      : '윜코드',
            "city"      : '서울',
            "state"     : '강남구',
            "price"     : 20,
            },
            {
            "imageUrl"  : None,
            "postingId" : 1,
            "job"       : '개발자구해요11',
            "name"      : '윜코드',
            "city"      : '서울',
            "state"     : '강남구',
            "price"     : 10,
            }
            ])
        
        self.assertEqual(response.status_code, 200)

    def test_posting_get_invalid_token(self):
        headers  = {'HTTP_AUTHORIZATION': 'asdf'}
        response = client.get('/main', **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['message'], 'INVALID_TOKEN')
    
    def test_posting_get_none_token(self):
        response = client.get('/main')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['message'], 'NEED_LOGIN')

    def test_posting_get_does_not_exists(self):
        token       = jwt.encode({'id':10}, SECRET_KEY, algorithm=ALGORITHM)
        headers     = {'HTTP_AUTHORIZATION': token}
        response    = client.get('/main', **headers)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['message'], 'DOES_NOT_EXISTS')

class DetailPaginationViewTest(TestCase):
    maxDiff=None
    def setUp(self):
        User.objects.create(
                            id    = 1, 
                            name  = 'dadewd', 
                            email = 'cat@cat'
                            )
        WorkExperience.objects.create(
                                      id   = 1, 
                                      name = 'aaaa'
                                      )
        Occupation.objects.create(
                                  id   = 1, 
                                  name = 'aaa'
                                  )
        JobCategory.objects.create(
                                   id         = 1, 
                                   occupation = Occupation.objects.get(id=1), 
                                   name       = 'bbb'
                                   )
        JobCategory.objects.create(
                                   id         = 2, 
                                   occupation = Occupation.objects.get(id=1), 
                                   name       = 'bbb'
                                   )
        State.objects.create(
                            id   = 1, 
                            name = 'aaa'
                            )
        County.objects.create(
                              id   = 1, 
                              name = 'aaaa'
                              )
        Company.objects.create(
                              id          = 1, 
                              name        = 'bbb', 
                              icon        = 'asesd', 
                              description = 'dases'
                              )
        Company.objects.create(
                              id          = 2, 
                              name        = 'bbb', 
                              icon        = 'asesd', 
                              description = 'dases'
                              )
        Company.objects.create(
                              id          = 3, 
                              name        = 'bbb', 
                              icon        = 'asesd', 
                              description = 'dases'
                              )
        Company.objects.create(
                              id          = 4, 
                              name        = 'bbb', 
                              icon        = 'asesd', 
                              description = 'dases'
                              )
        Company.objects.create(
                              id          = 5, 
                              name        = 'bbb', 
                              icon        = 'asesd', 
                              description = 'dases'
                              )
        Company.objects.create(
                              id          = 6, 
                              name        = 'bbb', 
                              icon        = 'asesd', 
                              description = 'dases'
                              )
        Company.objects.create(
                              id          = 7, 
                              name        = 'bbb', 
                              icon        = 'asesd', 
                              description = 'dases'
                              )
        CompanyImage.objects.create(
                                    id        = 1,
                                    company   = Company.objects.get(id=1), 
                                    image_url = 'asdefafasd'
                                    )
        CompanyImage.objects.create(
                                    id        = 2,
                                    company   = Company.objects.get(id=2), 
                                    image_url = 'asdefafasd'
                                    )
        CompanyImage.objects.create(
                                    id        = 3,
                                    company   = Company.objects.get(id=3), 
                                    image_url = 'asdefafasd'
                                    )
        CompanyImage.objects.create(
                                    id        = 4,
                                    company   = Company.objects.get(id=4), 
                                    image_url = 'asdefafasd'
                                    )
        CompanyImage.objects.create(
                                    id        = 5,
                                    company   = Company.objects.get(id=5), 
                                    image_url = 'asdefafasd'
                                    )
        CompanyImage.objects.create(
                                    id=6,
                                    company=Company.objects.get(id=6), 
                                    image_url='asdefafasd'
                                    )
        CompanyImage.objects.create(
                                    id        = 7,
                                    company   = Company.objects.get(id=7), 
                                    image_url = 'asdefafasd'
                                    )
        CompanyDetail.objects.create(
                                    id        = 1,
                                    company   = Company.objects.get(id=1), 
                                    name      = 'ijonkm', 
                                    address   = 'asdqwndinm', 
                                    latitude  = 34, 
                                    longitude = 56, 
                                    state     = State.objects.get(id=1), 
                                    county    = County.objects.get(id=1)
                                    )
        CompanyDetail.objects.create(
                                    id        = 2,
                                    company   = Company.objects.get(id=2), 
                                    name      = 'ijonkm', 
                                    address   = 'asdqwndinm', 
                                    latitude  = 34, 
                                    longitude = 56, 
                                    state     = State.objects.get(id=1), 
                                    county    = County.objects.get(id=1)
                                    )
        CompanyDetail.objects.create(
                                    id        = 3,
                                    company   = Company.objects.get(id=3), 
                                    name      = 'ijonkm', 
                                    address   = 'asdqwndinm', 
                                    latitude  = 34, 
                                    longitude = 56, 
                                    state     = State.objects.get(id=1), 
                                    county    = County.objects.get(id=1)
                                    )
        CompanyDetail.objects.create(
                                    id        = 4,
                                    company   = Company.objects.get(id=4), 
                                    name      = 'ijonkm', 
                                    address   = 'asdqwndinm', 
                                    latitude  = 34, 
                                    longitude = 56, 
                                    state     = State.objects.get(id=1), 
                                    county    = County.objects.get(id=1)
                                    )
        CompanyDetail.objects.create(
                                    id        = 5,
                                    company   = Company.objects.get(id=5), 
                                    name      = 'ijonkm', 
                                    address   = 'asdqwndinm', 
                                    latitude  = 34, 
                                    longitude = 56, 
                                    state     = State.objects.get(id=1), 
                                    county    = County.objects.get(id=1)
                                    )
        CompanyDetail.objects.create(
                                    id        = 6,
                                    company   = Company.objects.get(id=6), 
                                    name      = 'ijonkm', 
                                    address   = 'asdqwndinm', 
                                    latitude  = 34, 
                                    longitude = 56, 
                                    state     = State.objects.get(id=1), 
                                    county    = County.objects.get(id=1)
                                    )
        CompanyDetail.objects.create(
                                    id        = 7,
                                    company   = Company.objects.get(id=7), 
                                    name      = 'ijonkm', 
                                    address   = 'asdqwndinm', 
                                    latitude  = 34, 
                                    longitude = 56, 
                                    state     = State.objects.get(id=1), 
                                    county    = County.objects.get(id=1)
                                    )
        Posting.objects.create(
                              id              = 1, 
                              title           = 'adnowpmpqwm', 
                              job_category    = JobCategory.objects.get(id=1), 
                              company_detail  = CompanyDetail.objects.get(id=1), 
                              work_experience = WorkExperience.objects.get(id=1),
                              reward          = 100, 
                              description     = 'asdeegmin', 
                              end_date        = '2021-04-03'
                              )
        Posting.objects.create(
                              id              = 2, 
                              title           = 'adnowpmpqwm', 
                              job_category    = JobCategory.objects.get(id=1), 
                              company_detail  = CompanyDetail.objects.get(id=2), 
                              work_experience = WorkExperience.objects.get(id=1),
                              reward          = 100, 
                              description     = 'asdeegmin', 
                              end_date        = '2021-04-03'
                              )
        Posting.objects.create(
                              id              = 3, 
                              title           = 'adnowpmpqwm', 
                              job_category    = JobCategory.objects.get(id=1), 
                              company_detail  = CompanyDetail.objects.get(id=3), 
                              work_experience = WorkExperience.objects.get(id=1),
                              reward          = 100, 
                              description     = 'asdeegmin', 
                              end_date        = '2021-04-03'
                              )
        Posting.objects.create(
                              id              = 4, 
                              title           = 'adnowpmpqwm', 
                              job_category    = JobCategory.objects.get(id=1), 
                              company_detail  = CompanyDetail.objects.get(id=4), 
                              work_experience = WorkExperience.objects.get(id=1),
                              reward          = 100, 
                              description     = 'asdeegmin', 
                              end_date        = '2021-04-03'
                              )
        Posting.objects.create(
                              id              = 5, 
                              title           = 'adnowpmpqwm', 
                              job_category    = JobCategory.objects.get(id=1), 
                              company_detail  = CompanyDetail.objects.get(id=5), 
                              work_experience = WorkExperience.objects.get(id=1),
                              reward          = 100, 
                              description     = 'asdeegmin', 
                              end_date        = '2021-04-03'
                              )
        Posting.objects.create(
                              id              = 6, 
                              title           = 'adnowpmpqwm', 
                              job_category    = JobCategory.objects.get(id=1), 
                              company_detail  = CompanyDetail.objects.get(id=6), 
                              reward          = 100, 
                              work_experience = WorkExperience.objects.get(id=1),
                              description     = 'asdeegmin', 
                              end_date        = '2021-04-03'
                              )
        Posting.objects.create(
                              id              = 7, 
                              title           = 'adnowpmpqwm', 
                              job_category    = JobCategory.objects.get(id=2), 
                              company_detail  = CompanyDetail.objects.get(id=7), 
                              reward          = 100, 
                              description     = 'asdeegmin', 
                              end_date        = '2021-04-03',
                              work_experience = WorkExperience.objects.get(id=1),
                              )
        
        Like.objects.create(user=User.objects.get(id=1), posting=Posting.objects.get(id=1))
        Like.objects.create(user=User.objects.get(id=1), posting=Posting.objects.get(id=3))
        Like.objects.create(user=User.objects.get(id=1), posting=Posting.objects.get(id=5))

    def tearDown(self):
        Like.objects.all().delete()
        User.objects.all().delete()
        Occupation.objects.all().delete()
        WorkExperience.objects.all().delete()
        JobCategory.objects.all().delete()
        State.objects.all().delete()
        County.objects.all().delete()
        Company.objects.all().delete()
        CompanyImage.objects.all().delete()
        CompanyDetail.objects.all().delete()
        Posting.objects.all().delete()


    def test_user_pagination_page_1_success(self):
        client   = Client()
        token    = jwt.encode({'id': User.objects.get(id=1).id}, SECRET_KEY, algorithm=ALGORITHM)
        response = client.get('/posting/1/related-posting?page=1', **{'HTTP_Authorization': token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'SUCCESS', 'data': 
            [
                {
                    'id'      : 2,
                    'image'   : 'asdefafasd',
                    'like'    : 0,
                    'title'   : 'adnowpmpqwm',
                    'company' : 'bbb',
                    'city'    : 'aaa',
                    'nation'  : 'aaaa', 
                    'bonus'   : 100,
                    'userLike': False,
                    },
                {
                    'id'      : 3,
                    'image'   : 'asdefafasd',
                    'like'    : 1,
                    'title'   : 'adnowpmpqwm',
                    'company' : 'bbb',
                    'city'    : 'aaa',
                    'nation'  : 'aaaa', 
                    'bonus'   : 100,
                    'userLike': True,
                    },
                {
                    'id'      : 4,
                    'image'   : 'asdefafasd',
                    'like'    : 0,
                    'title'   : 'adnowpmpqwm',
                    'company' : 'bbb',
                    'city'    : 'aaa',
                    'nation'  : 'aaaa', 
                    'bonus'   : 100,
                    'userLike': False,
                    },
                {
                    'id'      : 5,
                    'image'   : 'asdefafasd',
                    'like'    : 1,
                    'title'   : 'adnowpmpqwm',
                    'company' : 'bbb',
                    'city'    : 'aaa',
                    'nation'  : 'aaaa', 
                    'bonus'   : 100,
                    'userLike': True,
                    },
                ]
            }
            )

    def test_nonuser_pagination_page_1_success(self):
        client   = Client()
        response = client.get('/posting/1/related-posting?page=1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'SUCCESS', 'data': 
            [
                {
                    'id'      : 2,
                    'image'   : 'asdefafasd',
                    'like'    : 0,
                    'title'   : 'adnowpmpqwm',
                    'company' : 'bbb',
                    'city'    : 'aaa',
                    'nation'  : 'aaaa', 
                    'bonus'   : 100,
                    'userLike': False,
                    },
                {
                    'id'      : 3,
                    'image'   : 'asdefafasd',
                    'like'    : 1,
                    'title'   : 'adnowpmpqwm',
                    'company' : 'bbb',
                    'city'    : 'aaa',
                    'nation'  : 'aaaa', 
                    'bonus'   : 100,
                    'userLike': False,
                    },
                {
                    'id'      : 4,
                    'image'   : 'asdefafasd',
                    'like'    : 0,
                    'title'   : 'adnowpmpqwm',
                    'company' : 'bbb',
                    'city'    : 'aaa',
                    'nation'  : 'aaaa', 
                    'bonus'   : 100,
                    'userLike': False,
                    },
                {
                    'id'      : 5,
                    'image'   : 'asdefafasd',
                    'like'    : 1,
                    'title'   : 'adnowpmpqwm',
                    'company' : 'bbb',
                    'city'    : 'aaa',
                    'nation'  : 'aaaa', 
                    'bonus'   : 100,
                    'userLike': False,
                    },
                ]
            }
            )

    def test_user_pagination_page_2_success(self):
        client   = Client()
        token    = jwt.encode({'id': User.objects.get(id=1).id}, SECRET_KEY, algorithm=ALGORITHM)
        response = client.get('/posting/1/related-posting?page=2', **{'HTTP_Authorization': token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'SUCCESS', 'data': 
            [
                {
                    'id'      : 6,
                    'image'   : 'asdefafasd',
                    'like'    : 0,
                    'title'   : 'adnowpmpqwm',
                    'company' : 'bbb',
                    'city'    : 'aaa',
                    'nation'  : 'aaaa', 
                    'bonus'   : 100,
                    'userLike': False,
                    },
                ]
            }
            )
    
    def test_nonuser_pagination_page_2_success(self):
        client   = Client()
        response = client.get('/posting/1/related-posting?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'SUCCESS', 'data': 
            [
                {
                    'id'      : 6,
                    'image'   : 'asdefafasd',
                    'like'    : 0,
                    'title'   : 'adnowpmpqwm',
                    'company' : 'bbb',
                    'city'    : 'aaa',
                    'nation'  : 'aaaa', 
                    'bonus'   : 100,
                    'userLike': False,
                    },
                ]
            }
            )

    def test_pagination_end(self):
        client   = Client()
        response = client.get('/posting/1/related-posting?page=3')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"message": "NO_MORE_POSTING"})

    def test_pagination_exception(self):
        client   = Client()
        response = client.get('/posting/100/related-posting?page=10')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"message": "BAD_REQUEST"})

class LikeViewTest(TestCase):
    def setUp(self):
        User.objects.create(
                            id    = 1, 
                            name  = 'gildong', 
                            email = 'cat@cat'
                            )
        Occupation.objects.create(
                                  id   = 1, 
                                  name = 'aaa'
                                  )
        WorkExperience.objects.create(
                                      id   = 1, 
                                      name = 'www'
                                      )
        JobCategory.objects.create(
                                  id         = 1, 
                                  occupation = Occupation.objects.get(id=1), 
                                  name       = 'aaa'
                                  )
        State.objects.create(
                            id   = 1, 
                            name = 'aaa'
                            )
        County.objects.create(
                              id   = 1, 
                              name = 'aaaa')
        Company.objects.create(
                              id          = 1, 
                              name        = 'aaa', 
                              icon        = 'asesd', 
                              description = 'dases'
                              )
        Company.objects.create(
                               id          = 2, 
                               name        = 'bbb', 
                               icon        = 'asesd', 
                               description = 'dases'
                               )
        CompanyImage.objects.create(
                                    id        = 1, 
                                    company   = Company.objects.get(id=1), 
                                    image_url = 'asdefafasd'
                                    )
        CompanyImage.objects.create(
                                    id        = 2, 
                                    company   = Company.objects.get(id=2), 
                                    image_url = 'asdefafasd'
                                    )
        CompanyDetail.objects.create(
                                    id        = 1, 
                                    company   = Company.objects.get(id=1), 
                                    name      = 'ijonkm', 
                                    address   = 'asdqwndinm', 
                                    latitude  = 34, 
                                    longitude = 56, 
                                    state     = State.objects.get(id=1), 
                                    county    = County.objects.get(id=1)
                                    )
        CompanyDetail.objects.create(
                                    id        = 2, 
                                    company   = Company.objects.get(id=2), 
                                    name      = 'ijonkm', 
                                    address   = 'asdqwndinm', 
                                    latitude  = 34, 
                                    longitude = 56, 
                                    state     = State.objects.get(id=1), 
                                    county    = County.objects.get(id=1)
                                    )
        Posting.objects.create(
                              id              = 1, 
                              work_experience = WorkExperience.objects.get(id=1), 
                              title           = 'adnowpmpqwm', 
                              job_category    = JobCategory.objects.get(id=1), 
                              company_detail  = CompanyDetail.objects.get(id=1), 
                              reward          = 100, 
                              description     = 'asdeegmin', 
                              end_date        = '2021-04-03'
                              )
        Posting.objects.create(
                              id              = 2, 
                              work_experience = WorkExperience.objects.get(id=1), 
                              title           = 'adnowpmpqwm', 
                              job_category    = JobCategory.objects.get(id=1), 
                              company_detail  = CompanyDetail.objects.get(id=2), 
                              reward          = 100, 
                              description     = 'asdeegmin', 
                              end_date        = '2021-04-03'
                              )
        Like.objects.create(
                           id      = 1, 
                           user    = User.objects.get(id=1), 
                           posting = Posting.objects.get(id=2)
                           )
        BookMark.objects.create(
                           id      = 1, 
                           user    = User.objects.get(id=1), 
                           posting = Posting.objects.get(id=2)
                           )
        

    def tearDown(self):
        Like.objects.all().delete()
        BookMark.objects.all().delete()
        Occupation.objects.all().delete()
        WorkExperience.objects.all().delete()
        JobCategory.objects.all().delete()
        State.objects.all().delete()
        County.objects.all().delete()
        Company.objects.all().delete()
        CompanyImage.objects.all().delete()
        CompanyDetail.objects.all().delete()
        Posting.objects.all().delete()
        User.objects.all().delete()

    def test_like_add_test(self):
        client   = Client()
        user     = User.objects.get(id=1)
        token    = jwt.encode({'id': user.id}, SECRET_KEY, algorithm=ALGORITHM)
        response = client.post('/posting/like/1', **{'HTTP_Authorization': token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'SUCCESS'})
    
    def test_bookmark_add_test(self):
        client   = Client()
        user     = User.objects.get(id=1)
        token    = jwt.encode({'id': user.id}, SECRET_KEY, algorithm=ALGORITHM)
        response = client.post('/posting/bookmark/1', **{'HTTP_Authorization': token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'SUCCESS'})
    
    def test_like_delete_test(self):
        client   = Client()
        user     = User.objects.get(id=1)
        token    = jwt.encode({'id': user.id}, SECRET_KEY, algorithm=ALGORITHM)
        response = client.post('/posting/like/2', **{'HTTP_Authorization': token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'WASTED'})
    
    def test_bookmark_delete_test(self):
        client   = Client()
        user     = User.objects.get(id=1)
        token    = jwt.encode({'id': user.id}, SECRET_KEY, algorithm=ALGORITHM)
        response = client.post('/posting/bookmark/2', **{'HTTP_Authorization': token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'WASTED'})

    def test_nonuser_bookmark_test(self):
        client   = Client()
        response = client.post('/posting/bookmark/1')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'NEED_LOGIN'})

    def test_nonuser_like_test(self):
        client   = Client()
        response = client.post('/posting/like/1')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'NEED_LOGIN'})

    def test_bookmark_exception(self):
        client   = Client()
        user     = User.objects.get(id=1)
        token    = jwt.encode({'id': user.id}, SECRET_KEY, algorithm=ALGORITHM)
        response = client.post('/posting/bookmark/100', **{'HTTP_Authorization': token})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'message': 'BAD_REQUEST'})

    def test_like_exception(self):
        client   = Client()
        user     = User.objects.get(id=1)
        token    = jwt.encode({'id': user.id}, SECRET_KEY, algorithm=ALGORITHM)
        response = client.post('/posting/like/100', **{'HTTP_Authorization': token})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'message': 'BAD_REQUEST'})
