import json
import jwt

from my_settings import SECRET_KEY, ALGORITHM

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        if 'Authorization' not in reqeust.headers:
            return JsonResponse({'message':'NEED_LOGIN'}, status=400)

        try:
            token        = request.headers['Authorization']
            check_token  = jwt.decode(token, SECRET_KEY, ALGORITHM)
            user         = User.objects.get(id=check_token['id'])
            requset.user = user

        except User.DoseNotExists:
            return JsonResponse({'message':'DOES_NOT_EXISTS'}, status=400)
        except jwt.DecodeError:
            return JsonResponse({'message':'INVALID_TOKEN'}, status=400)
        
        return func(self, request, *args, **kwargs)
    
    return wrapper
