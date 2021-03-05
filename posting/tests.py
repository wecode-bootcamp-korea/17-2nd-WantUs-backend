import unittest
import jwt

from django.test import TestCase, Client

from user.models import User, WorkExperience
from posting.models import (BookMark, Posting, JobCategory, Occupation,
                            Company, CompanyDetail, CompanyImage,
                            State, County, Like,
                            Tag, TagDetail, CompanyTag)
from my_settings  import SECRET_KEY, ALGORITHM

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
        token    = jwt.encode({'user_id': User.objects.get(id=1).id}, SECRET_KEY, algorithm=ALGORITHM)
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
                'userLike'     : True,
                'userBookmark' : True
                        }
            ]
            }
            )
    
    def test_postingdetail_nonliked_get_success(self):
        client   = Client()
        token    = jwt.encode({'user_id': User.objects.get(id=1).id}, SECRET_KEY, algorithm=ALGORITHM)
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
                'latitude'     : 34,
                'longitude'    : 56,
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
