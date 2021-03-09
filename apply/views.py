import json
from django.http        import JsonResponse
from django.views       import View
from django.db.models   import Count

from .models        import (
        Apply,
        ProcessStatus
        )
from user.models    import User
from utils          import login_decorator
from resume.models  import Resume, ResumeFile
from posting.models import (
        Posting,
        Occupation,
        JobCategory,
        CompanyImage,
        CompanyDetail,
        State,
        County,
        Tag,
        TagDetail,
        CompanyTag,
        BookMark,
        Like,
        Company,
        )

class ApplyView(View):
    @login_decorator
    def get(self, request):
        user = request.user

        resumes     = Resume.objects.filter(user=user).values(\
                        'id', 'user_id', 'title', 'introduce', 'create_at')
        resume_file = ResumeFile.objects.filter(user=user).values(\
                        'id', 'user_id', 'title', 'file_url', 'create_at')
        
        resume_result = []

        for resume in resumes.union(resume_file).order_by('-create_at'):
            result = {
                'id'        : resume['id'],
                'userId'    : resume['user_id'],
                'title'     : resume['title'],
                'createAt'  : resume['create_at'],
                'introduce' : resume['introduce'] if resume.get('introduce') else '',
                'file_url'  : resume['file_url'] if resume.get('file_url') else '',
            }
            resume_result.append(result)

        data = {
            'name'        : user.name,
            'email'       : user.email,
            'phoneNumber' : user.phone_number,
            'resumes'     : resume_result
        }

        return JsonResponse({'message':'SUCCESS', 'data':data}, status=200)

    @login_decorator
    def post(self, request):
        data = json.loads(request.body)

        user    = request.user
        posting = data.get('posting', None)

        if not posting:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

        Apply.objects.create(
            user = user,
            posting_id = posting
        )

        return JsonResponse({'message':'SUCCESS'}, status=200)

class MyWantUsView(View):
    @login_decorator
    def get(self, request):
        user    = request.user
        user_info = {
                'profile'       : user.image_url,
                'name'          : user.name,
                'email'         : user.email,
                'phoneNumber'   : user.phone_number
                }
        
        FIRST  = '지원 완료'
        SECOND = '서류 통과'
        THIRD  = '최종 합격'
        FOURTH = '불합격'

        apply_list = {
                "stepOne"   : user.apply_set.filter(process_status__name = FIRST).count(),
                "stepTwo"   : user.apply_set.filter(process_status__name = SECOND).count(),
                "stepThree" : user.apply_set.filter(process_status__name = THIRD).count(),
                "stepFour"  : user.apply_set.filter(process_status__name = FOURTH).count()
                }

        DATETIME_ONLY_TIME = 10
        book_mark_posting = [{
            'id'            : posting.id,
            'category'      : posting.job_category.occupation.name,
            'city'          : posting.company_detail.state.name,
            'company'       : posting.company_detail.company.name,
            'end'           : str(posting.end_date)[:DATETIME_ONLY_TIME],
            'image'         : posting.company_detail.company.companyimage_set.all()[0].image_url,
            'state'         : posting.company_detail.county.name,
            'subCategory'   : posting.job_category.name,
            'tags'          : [TagDetail.objects.get(id=tag_detail_id_dict['tag_detail_id']).name
                                for tag_detail_id_dict in posting.company_detail.company.companytag_set.values()],
            'title'         : posting.title,
            } for posting in Posting.objects.filter(bookmark__user = user).select_related('company_detail', 'company_detail__company', 'company_detail__state', 'company_detail__county', 'job_category__occupation').prefetch_related('company_detail__company__companyimage_set','company_detail__company__companytag_set')]
        
        like_posting = [{
            'id'        : posting.id,
            'city'      : posting.company_detail.state.name,
            'company'   : posting.company_detail.company.name,
            'image'     : posting.company_detail.company.companyimage_set.all()[0].image_url,
            'state'     : posting.company_detail.county.name,
            'title'     : posting.title,
            } for posting in Posting.objects.filter(like__user=user).select_related('company_detail','company_detail__company','company_detail__state','company_detail__county').prefetch_related('company_detail__company__companyimage_set')]

        return JsonResponse({'user' : user_info, "apply" : apply_list, "book" : book_mark_posting, "like" : like_posting}, status=200)
