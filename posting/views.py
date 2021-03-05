import json
import math

from django.http           import JsonResponse, HttpResponse
from django.views          import View
from django.core.paginator import Paginator

from posting.models        import Posting, Like, BookMark
from utils                 import non_user_accept_decorator

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
