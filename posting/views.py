import json
import math

from django.core.paginator  import Paginator
from django.http            import JsonResponse
from django.views           import View
from django.db.models       import Count

from user.models    import User
from utils          import login_decorator, non_user_accept_decorator
from posting.models import (
        Posting,
        Occupation,
        Company,
        CompanyImage,
        CompanyDetail,
        State,
        County,
        Like,
        BookMark
)

class PostingDetailView(View):
    @non_user_accept_decorator
    def get(self, request, posting_id):
        try:
            user     = request.user
            posting  = Posting.objects.get(id=posting_id)
            result   = []
            contents = {
                    'id'           : posting.id,
                    'title'        : posting.title,
                    'company'      : posting.company_detail.company.name,
                    'city'         : posting.company_detail.state.name,
                    'district'     : posting.company_detail.county.name,
                    'detailAddress': posting.company_detail.address,
                    'latitude'     : float(posting.company_detail.latitude),
                    'longitude'    : float(posting.company_detail.longitude),
                    'tags'         : [tag_detail.name for tag_detail in posting.company_detail.company.tag.all()],
                    'description'  : posting.description,
                    'image'        : posting.company_detail.company.companyimage_set.first().image_url,
                    'bonus'        : int(posting.reward),
                    'like'         : posting.like_set.count(),
                    'deadline'     : str(posting.end_date)[:10],
                    'logoSrc'      : posting.company_detail.company.icon,
                    'category'     : posting.job_category.occupation.name,
                        }
            if user is None:
                contents['user']         = user
                contents['userLike']     = False
                contents['userBookmark'] = False
                result.append(contents)
                return JsonResponse({"message": "SUCCESS", "data": result}, status=200)

            contents['user']         = user.name
            contents['userLike']     = True if Like.objects.filter(user=user, posting=posting).exists() else False
            contents['userBookmark'] = True if BookMark.objects.filter(user=user, posting=posting).exists() else False
            result.append(contents)
            return JsonResponse({"message": "SUCCESS", "data": result}, status=200)
            
        except Posting.DoesNotExist:
            return JsonResponse({"message": "BAD_REQUEST"}, status=404) 

LIST_LIMIT_NUMBER = 4

class MainView(View):
    @login_decorator
    def get(self, request):
        set_postings = Posting.objects.annotate(like_num=Count("like")).\
                    select_related('company_detail', 
                            'company_detail__state', 
                            'company_detail__county', 
                            'company_detail__company', 
                            'job_category', 
                            'job_category__occupation').all()

        postings = set_postings.order_by('-like_num')[:LIST_LIMIT_NUMBER]

        like_posting_list = [{
            "postingId" : posting.id,
            "imageUrl"  : posting.company_detail.company.companyimage_set.first().image_url if posting.company_detail.company.companyimage_set.exists() else None,
            "job"       : posting.title,
            "name"      : posting.company_detail.company.name,
            "city"      : posting.company_detail.state.name,
            "state"     : posting.company_detail.county.name,
            "price"     : int(posting.reward),
            "likeNum"   : posting.like_set.filter(posting=posting).count()
            } for posting in postings]

        postings = set_postings.order_by('-create_at')[:LIST_LIMIT_NUMBER]

        new_company_list = [{
            "postingId" : posting.id,
            "imageUrl"  : posting.company_detail.company.companyimage_set.first().image_url if posting.company_detail.company.companyimage_set.exists() else None,
            "name"      : posting.company_detail.company.name,
            "job"       : posting.job_category.occupation.name,
            }for posting in postings]

        new_posting_list = [{
            "imageUrl"  : posting.company_detail.company.companyimage_set.first().image_url if posting.company_detail.company.companyimage_set.exists() else None,
            "postingId" : posting.id,
            "job"       : posting.title,
            "name"      : posting.company_detail.company.name,
            "city"      : posting.company_detail.state.name,
            "state"     : posting.company_detail.county.name,
            "price"     : int(posting.reward),
            } for posting in postings]

        return JsonResponse({"likePosting" : like_posting_list, "new" : new_company_list, "thisWeek" : new_posting_list}, status=200)
