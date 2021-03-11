import json
import math

from django.core.paginator  import Paginator
from django.http            import JsonResponse
from django.views           import View
from django.db.models       import (
    Count,
    Prefetch,
    Q
)

from posting.models import (
    Posting, 
    CompanyDetail, 
    CompanyTag,
    County,
    State,
    Tag,
    TagDetail,
    JobCategory
)
from user.models            import User
from resume.models          import Resume, ResumeFile, ResumeStatus
from utils                  import login_decorator, non_user_accept_decorator
from posting.models         import (
        Posting,
        Occupation,
        Company,
        CompanyImage,
        CompanyDetail,
        State,
        County,
        Like,
        BookMark,
        CompanyTag,
        Tag,
        TagDetail
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
                contents['user']         = None
                contents['userLike']     = False
                contents['userBookmark'] = False
                result.append(contents)
                return JsonResponse({"message": "SUCCESS", "data": result}, status=200)
            
            contents['user']         = user.name
            contents['userLike']     = True if Like.objects.filter(user=user, posting=posting).exists() else False
            contents['userBookmark'] = True if BookMark.objects.filter(user=user, posting=posting).exists() else False
            contents['userEmail']    = user.email
            contents['userPhone']    = user.phone_number
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

class RelatedPostingView(View):
    @non_user_accept_decorator
    def get(self, request, posting_id):
        PER_PAGE = 4
        try:
            user            = request.user
            posting         = Posting.objects.get(id=posting_id)
            posting_related = Posting.objects.filter(job_category=posting.job_category).exclude(id=posting_id).order_by('id')
            limit_page      = math.ceil(posting_related.count()/PER_PAGE)
            page            = request.GET['page']
            paginator       = Paginator(posting_related, PER_PAGE)

            if int(page) > limit_page:
                return JsonResponse({"message": "NO_MORE_POSTING"}, status=404)
            
            posting_related = paginator.get_page(page)
            posting_list    = [
                        {
                        'id'     : posting_related.id,
                        'image'  : posting_related.company_detail.company.companyimage_set.first().image_url,
                        'like'   : posting_related.like_set.count(),
                        'title'  : posting_related.title, 
                        'company': posting_related.company_detail.company.name,
                        'city'   : posting_related.company_detail.state.name,
                        'nation' : posting_related.company_detail.county.name,
                        'bonus'  : int(posting_related.reward),
                        'userLike' : True if Like.objects.filter(user=user, posting=posting_related).exists() else False,
                        } for posting_related in posting_related]
            return JsonResponse({"message": "SUCCESS", "data": posting_list}, status=200)

        except Posting.DoesNotExist:
            return JsonResponse({"message": "BAD_REQUEST"}, status=404)

class PostingLikeView(View):
    @login_decorator
    def post(self, request, posting_id):
        try:
            user    = request.user
            posting = Posting.objects.get(id=posting_id)
            
            if Like.objects.filter(user=user, posting=posting).exists():
                Like.objects.filter(user=user, posting=posting).delete()
                return JsonResponse({"message": "WASTED"}, status=200)
            
            posting.posting_like.add(user)
            return JsonResponse({"message": "SUCCESS"}, status=200)
        
        except Posting.DoesNotExist:
            return JsonResponse({'message': 'BAD_REQUEST'}, status=404)

class PostingBookmarkView(View):
    @login_decorator
    def post(self, request, posting_id):
        try:
            user    = request.user
            posting = Posting.objects.get(id=posting_id)
            
            if BookMark.objects.filter(user=user, posting=posting).exists():
                BookMark.objects.filter(user=user, posting=posting).delete()
                return JsonResponse({"message": "WASTED"}, status=200)
            
            posting.posting_mark.add(user)
            return JsonResponse({"message": "SUCCESS"}, status=200)
        
        except Posting.DoesNotExist:
            return JsonResponse({'message': 'BAD_REQUEST'}, status=404)

class PostingListView(View):
    def get(self, request):
        q = Q()

        category        = request.GET.get('category', '전체')
        sorting         = request.GET.get('sorting', 'new')
        tags            = request.GET.getlist('tag', None)
        locations       = request.GET.getlist('location', None)

        if category != '전체':
            q.add(Q(job_category__name = category), q.AND)

        query = Posting.objects.filter(q)

        if locations:
            query = Posting.objects.filter(company_detail__county__name__in=locations)

        if tags:
            for tag in tags:
                query = query.filter(company_detail__company__tag__name=tag)
            
        SORTING_DICT = {
            'new'     : '-create_at',
            'popular' : '-like_num',
            'reward'  : '-reward'
        }

        page      = request.GET.get('page', 1)
        per_page  = request.GET.get('per_page', 30)

        postings = query.select_related\
                    ('company_detail', 'company_detail__company', 'company_detail__state', 'company_detail__county')\
                    .prefetch_related('company_detail__company__companyimage_set', 'company_detail__company__companytag_set')\
                    .annotate(like_num=Count('posting_like'))\
                    .order_by(SORTING_DICT[sorting])

        paginator = Paginator(postings, per_page)

        if paginator.num_pages < int(page):
            return JsonResponse({'message':'NONE_PAGE'}, status=204)
        
        postings  = paginator.get_page(page)

        states      = State.objects.all()
        counties    = County.objects.all()
        filter_tags = Tag.objects.all()

        data = {
            'postings' : [{
                'id'      : posting.id,
                'like'    : posting.like_set.filter(posting=posting).count(),
                'title'   : posting.title,
                'company' : posting.company_detail.company.name,
                'state'   : posting.company_detail.state.name,
                'county'  : posting.company_detail.county.name,
                'reward'  : posting.reward,
                'image'   : [company_image.image_url for company_image in posting.company_detail.company.companyimage_set.all()]
            } for posting in postings],
            'locations' : {
                'state' : [{
                    'id'   : state.id,
                    'name' : state.name
                } for state in states],
                'county' : [{
                    'id'   : county.id,
                    'name' : county.name
                } for county in counties],
            },
            'tags' : [{
                    'id'   : tag.id,
                    'name' : tag.name,
                    'tagDetails' : [{
                        'id'   : tag_detail.id,
                        'name' : tag_detail.name
                    } for tag_detail in tag.tagdetail_set.all()]
                } for tag in filter_tags],
            'categories' : [{
                'id' : category.id,
                'name' : category.name
            } for category in JobCategory.objects.all()]
        }

        return JsonResponse({'message':'SUCCESS', 'data':data}, status=200)
        
