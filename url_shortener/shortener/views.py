import json
import jwt
import random
import string
from datetime import datetime, timedelta

from django.conf.global_settings import SECRET_KEY
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

from shortener.config import token_required
from shortener.exceptions import JsonBadRequestResponse, JsonMethodNotAllowedResponse, JsonResourceNotFoundResponse
from shortener.models import Urls


def home(request, short):
    url = Urls.objects.filter(short_form='http://localhost:8000/visit/' + short).first()
    url.nbr_visit += 1
    url.save()
    return redirect("https://" + url.original_form)


@csrf_exempt
def register(request):
    if not request.method == 'POST':
        return JsonMethodNotAllowedResponse({'message': 'method not allowed', 'status': 405})

    data = json.loads(request.body)
    if not data.get('name') or not data.get('password'):
        return JsonBadRequestResponse({'message': 'name or password is missing', 'status': 400})

    user = User(username=data.get('name'), password=data.get('password'))
    user.save()
    return JsonResponse({'message': 'user registered successfully', 'status': 201})


@csrf_exempt
def login(request):
    if not request.method == 'POST':
        return JsonMethodNotAllowedResponse({'message': 'method not allowed', 'status': 405})

    data = json.loads(request.body)
    if not data.get('name') or not data.get('password'):
        return JsonBadRequestResponse({'message': 'name or password is missing', 'status': 400})

    user = User.objects.filter(username=data.get('name')).first()
    if not user:
        return JsonResourceNotFoundResponse({'message': 'no user found with name ' + data.get('name'), 'status': 404})

    token = jwt.encode({'name': user.username, 'exp': datetime.utcnow() + timedelta(days=5)}, SECRET_KEY)
    user_dict = {'id': user.id, 'name': user.username}
    jwt_token = {'type': 'Bearer', 'token': token.decode('UTF-8')}
    response = {'user': user_dict, 'token': jwt_token}
    return JsonResponse(response)


@csrf_exempt
def shorten(request):
    current_user = token_required(request)
    if not current_user:
        return JsonBadRequestResponse({'message': 'wrong jwt', 'status': 400})
    if not request.method == 'POST':
        return JsonMethodNotAllowedResponse({'message': 'method not allowed', 'status': 405})

    data = json.loads(request.body)
    if not data.get('url'):
        return JsonBadRequestResponse({'message': 'url to shorten is missing', 'status': 400})

    random_string = "".join(random.choice(string.ascii_letters) for i in range(6))
    url = Urls(short_form='http://localhost:8000/visit/' + random_string, original_form=data.get('url'),
               user_id=current_user.id)
    url.save()
    return JsonResponse({'url': 'http://localhost:8000/visit/' + random_string, 'status': 200})


def stat(request, short):
    current_user = token_required(request)
    if not current_user:
        return JsonBadRequestResponse({'message': 'wrong jwt', 'status': 400})

    if not request.method == 'GET':
        return JsonMethodNotAllowedResponse({'message': 'method not allowed', 'status': 405})

    url = Urls.objects.filter(short_form='http://localhost:8000/visit/' + short).first()
    response = {'short_for': url.short_form, 'original_form': url.original_form, 'nbr_visit': url.nbr_visit}
    return JsonResponse(response)
