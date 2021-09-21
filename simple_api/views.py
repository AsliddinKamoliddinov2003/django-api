import json
from django.http.response import JsonResponse
import hashlib
import random
from django.contrib.auth import get_user_model

from . import models
from .decorators import token_auth
from django.views.decorators.csrf import csrf_exempt


def serialize_book(obj, many=False, fields=["id", "title", "release_year", "rating", "created_at", "updated_at"]):

    if many:
        data = []
        for book in obj:
            temp = {}
            for field in fields:
                if hasattr(book, field):
                    temp[field]=getattr(book, field)

            data.append(temp)

    else:
        data = {}
        for field in fields:
            if hasattr(obj, field):
                data[field]=getattr(obj, field)

    return data


@csrf_exempt
def books(request):
    if request.method == "GET":
        books = models.Book.objects.all()
        data = serialize_book(books, many=True)
        return JsonResponse(data, safe=False)

    elif request.method == "POST":
        body = json.loads(request.body)
        title = body.get("title", "")
        release_year = body.get("release_year", 0)
        rating = body.get("rating", 0.0)
        category_id = body.get("category",0)

        category = models.Category.objects.get(id=category_id)
        book = models.Book(
            title=title,
            release_year=release_year,
            rating=rating,
            category=category
        )

        book.save()
        data = serialize_book(book)
        return JsonResponse(data)
       

@csrf_exempt
@token_auth
def book(request, _id):
    book = models.Book.objects.get(id=_id)
    
    if request.method == "GET":
        data = serialize_book(book, fields=["id", "title", "rating"])
        return JsonResponse(data)

        
    elif request.method == "PUT":
        
        body = json.loads(request.body)

        category_id = body.get("category",0)
        category = models.Category.objects.get(id=category_id)

        book.title = body.get("title","")
        book.release_year = body.get("release_year", 0)
        book.rating = body.get("rating",0.0)
        book.category = category
        book.save()
        data = serialize_book(book, fields=["title"])
        return JsonResponse(data)

        
    elif request.method == "PATCH":

        body = json.loads(request.body)

        title = body.get("title", "")
        release_year = body.get("release_year", 0)
        rating = body.get("rating", 0.0)
        category_id = body.get("category",0)

        # category = models.Category.objects.get(id=category_id)
        
        if title:
            book.title = title

        if release_year:
            book.release_year = release_year
        
        if rating:
            book.rating = rating

        book.save()
        data = serialize_book(book)
        return JsonResponse(data)

    elif request.method == "DELETE":
        data = serialize_book(book)
        book.delete()
        return JsonResponse(data)


User = get_user_model()

@csrf_exempt
def login(request):
    data = json.loads(request.body)

    username = data["username"]
    password = data["password"]
    
    user = User.objects.filter(username=username)

    if user.exists():
        user = user.first()
        if user.check_password(password):
            token = models.Token.objects.filter(user=user)
            if token.exists():
                token = token.first()
            else:
                hash = hashlib.sha224((username + password + str(random.randint(1, 9999))).encode()).hexdigest()
                token = models.Token(user=user, token = hash)
                token.save()

            return JsonResponse({ "token" : token.token })


    return JsonResponse({"error":"bunday user yo'q"})





        

        




        













