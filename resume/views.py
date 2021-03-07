from django.http        import JsonResponse
from django.views       import View
from django.db.models   import Count, Prefetch

from user.models    import User
from utils          import login_decorator
from resume.models  import (
        Resume,
        )

class ResumeMainView(View):
    @login_decorator
    def get(self, request):
        user    = request.user
        resumes = Resume.objects.filter(user=user)

        resume_list = [{
            "name" : resume.title,
            "data" : resume.update_at,
            "status" : resume.complete_status.status_code
            } for resume in resumes]

        return JsonResponse({'message' : resume_list}, status=200)
    @login_decorator
    def post(self, request):
        user    = request.user
        Resume.objects.create(
                user    = user,
                title   = f'{user.name}의 이력서'+str(Resume.objects.filter(user=user).count()+1),
                introduce = '내용을 채워주세요'
                )
        return JsonResponse({'message' : 'SUCCESS'}, status=201)
