import json
import jwt
import requests

from django.http  import JsonResponse
from django.views import View

from my_settings  import SECRET_KEY, ALGORITHM
from user.models  import User

class SignView(View):
    def get(self, request):
        try:
            kakao_token  = request.headers["Authorization"]
            headers      = {'Authorization' : f"Bearer {kakao_token}"}
            url          = "https://kapi.kakao.com/v2/user/me"
            response     = requests.request("GET", url, headers=headers)
            user         = response.json()

            if User.objects.filter(email = user['kakao_account']['email']).exists(): 
                user_info   = User.objects.get(email=user['kakao_account']['email'])
                encoded_jwt = jwt.encode({'id': user_info.id}, SECRET_KEY, algorithm=ALGORITHM)
                return JsonResponse({'message':'SUCCESS', 'accessToken' : encoded_jwt}, status = 200)
            
            new_user_info = User.objects.create(
                email     = user['kakao_account']['email'],
                name      = user['kakao_account']['profile']['nickname'],
                image_url = user['kakao_account']['profile'].get('profile_image_url', ''),
            )
            
            encoded_jwt = jwt.encode({'id': new_user_info.id}, SECRET_KEY, algorithm=ALGORITHM)
            return JsonResponse({'message':'SUCCESS', 'accessToken' : encoded_jwt}, status = 201)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status = 400)
