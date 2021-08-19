import jwt
from django.conf.global_settings import SECRET_KEY
from django.contrib.auth.models import User


def token_required(request):
    token = None

    if 'Authorization' in request.headers:
        token = request.headers.get('Authorization')

    if not token:
        return None

    try:
        data = jwt.decode(token[7:], SECRET_KEY)
        current_user = User.objects.filter(username=data.get('name')).first()
    except:
        return None

    return current_user
