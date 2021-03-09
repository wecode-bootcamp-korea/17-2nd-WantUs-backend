import json

from django.views import View
from django.http  import JsonResponse

from apply.models  import Apply
from resume.models import (
    Resume,
    ResumeFile
)
from utils         import login_decorator

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
                'id'        : resume.id,
                'userId'    : resume.user_id,
                'title'     : resume.title,
                'createAt'  : resume.create_at,
                'introduce' : resume.introduce if resume.get('introduce') else '',
                'file_url'  : resume.file_url if resume.get('file_url') else '',
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