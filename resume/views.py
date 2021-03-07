import uuid
import boto3

from django.http   import JsonResponse, HttpResponse
from django.views  import View

from my_settings   import S3KEY, S3SECRETKEY
from resume.models import ResumeFile
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
