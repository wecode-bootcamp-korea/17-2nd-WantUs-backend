import json
import jwt

from django.http import JsonResponse

from my_settings import SECRET_KEY, ALGORITHM
from user.models import User

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        if 'Authorization' not in request.headers:
            return JsonResponse({'message':'NEED_LOGIN'}, status=400)

        try:
            token        = request.headers['Authorization']
            check_token  = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
            user         = User.objects.get(id=check_token['id'])
            request.user = user

        except User.DoesNotExist:
            return JsonResponse({'message':'DOES_NOT_EXISTS'}, status=400)
        except jwt.DecodeError:
            return JsonResponse({'message':'INVALID_TOKEN'}, status=400)
        
        return func(self, request, *args, **kwargs)
    
    return wrapper

def non_user_accept_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token    = request.headers.get('Authorization', None)
            if not access_token:
                request.user = None
                return func(self, request, *args, **kwargs)

            payload         = jwt.decode(access_token, SECRET_KEY, algorithms=ALGORITHM)
            login_user      = User.objects.get(id=payload['id'])
            request.user    = login_user

        except jwt.DecodeError:
            return JsonResponse({'message' : 'INVALID_TOKEN'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_USER'}, status=401)

        return func(self, request, *args, **kwargs)

    return wrapper
