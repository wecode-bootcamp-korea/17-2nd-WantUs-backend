import uuid
import boto3

from django.http   import JsonResponse, HttpResponse
from django.views  import View

from my_settings   import S3KEY, S3SECRETKEY
from resume.models  import (
        ResumeFile,
        Resume,
        Career,
        Language,
        Education
        )
from user.models   import User
from utils         import login_decorator

class ResumeFilewUploadView(View):
    @login_decorator
    def post(self, request):
        user = request.user
        
        if request.FILES.__len__() == 0:
            return JsonResponse({"message": "FILE_DOES_NOT_EXIST"}, status=400)

        file = request.FILES['resume']
        
        if file.name.find('pdf') < 0:
            return JsonResponse({"message": "PLEASE_UPLOAD_PDF"}, status=400)
        
        s3_client = boto3.client(
            's3',
            aws_access_key_id = S3KEY,
            aws_secret_access_key = S3SECRETKEY
            )
        url_generator = str(uuid.uuid4())
        s3_client.upload_fileobj(
                file,  
                "wantusfile",
                url_generator,
                ExtraArgs = {
                    "ContentType": file.content_type,
                    }
                )

        file_url = f"https://wantusfile.s3.ap-northeast-2.amazonaws.com/{url_generator}"
        resume   = ResumeFile.objects.create(user=user, title=file.name, file_url=file_url, uuidcode=url_generator)
        return JsonResponse({'message': 'SUCCESS', 'data': file_url}, status=200)

class ResumePartialView(View):
   @login_decorator
   def get(self, request, resume_id):
        try:
            user                = request.user
            resume              = Resume.objects.get(id=resume_id)
            
            if user.id != resume.user.id:
                return JsonResponse({'message' : 'INVALID_USER'}, status=400)
            
            content = {
                    "userInfo" : {
                        "name"          : user.name,
                        "email"         : user.email,
                        "phoneNumber"   : user.phone_number
                    },
                    "resumeIntro" : resume.introduce,
                    "resumeTitle" : resume.title,
                    "career" : [{
                        "id"      : career.id,
                        "Name"    : career.name,
                        "Start"   : career.start_date,
                        "End" : career.end_date
                        } for career in resume.career_set.all()],
                    "education" : [{
                        "id"       : education.id,
                        "Name"     : education.name,
                        "Start"    : education.start_date,
                        "End"      : education.end_date
                        } for education in resume.education_set.all()],
                    "language" : [{
                        "id"    : language.id,
                        "Name"  : language.name,
                        "Start" : language.start_date,
                        "End"   : language.end_date
                        } for language in resume.language_set.all()]
                }
            return JsonResponse({'message' : 'SUCCESS', 'result' : content}, status=200)
        
        except Resume.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_RESUME'}, status=400)
