from . import models
from django.http import JsonResponse


def token_auth(view_func):
    def wrapper(request, *args, **kwargs):
        headers = request.headers
        auth = headers.get("Authorization")
        if auth:
            token = auth.split()[1]
            token_obj = models.Token.objects.filter(token=token)

            if not token_obj.exists():
                return JsonResponse({"error":"the token is invalid"})
            
            return view_func(request, *args, **kwargs)
        else:
            return JsonResponse({"error":"please, provide the auth header"})

    return wrapper